<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const UPLOAD_BASE_PATH = '/var/uploads/';
const THUMBNAILS_BASE_PATH = '/var/uploads/thumbnails/';
const PYTHON_PLACEHOLD = '***|||RESULT|||***';
/**
 *
 * @property Inv_item_model $inv_item_model
 * @property Inv_user_model $inv_user_model
 * @property Inv_recommendation_model $inv_recommendation_model
 */
class Inv2 extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'inv_item_model' );
		$this->load->model ( 'inv_user_model' );
		$this->load->model ( 'inv_recommendation_model' );
	}
	
	public function index()
	{
		$this->load->helper('form');
		$this->load->library('session');
		
		if ($this->input->post('submit')) {
			$where = $this->input->post ( 'where' );
			$this->session->set_userdata('QUERY_WHERE', $where);
		} else {
			$where = $this->session->userdata('QUERY_WHERE');
		}
		
		//"inv_item.itemId <> 3";
		$data['invs'] = $this->inv_item_model->get_available_inv_list($where);
		$data['count'] = $this->inv_item_model->count_available_inv_list($where);
		$data['title'] = 'Inv List';
		$data['where'] = $where;

		$this->load->view('templates/header', $data);
		$this->load->view('inv2/index', $data);
		$this->load->view('templates/footer');
	}
	
	public function details($userId, $itemId)
	{
		$data['inv'] = $this->inv_item_model->get_inv_item($userId, $itemId);
		if (empty($data['inv']))
		{
			show_404();
		}
		$data['title'] = 'Inv Details';
		
		$categories_ori = $this->call_query_categories_scritp($data['inv']['title']);
		$categories = array('' => 'Please select one category...');
		foreach ($categories_ori as $category) {
			$categories[$category['catNum']] = $category['catNameLong'];
		}
		$data['categories'] = $categories;
		
		$this->load->helper('form');
		
		$this->load->view('templates/header', $data);
		$this->load->view('inv2/details', $data);
		$this->load->view('templates/footer');
	}
	
	public function query_items($userId, $itemId, $catNum)
	{
		$data['inv'] = $this->inv_item_model->get_inv_item($userId, $itemId);
		if (empty($data['inv']))
		{
			show_404();
		}
		
		$data['match_items'] = $this->call_query_items_script($data['inv']['title'], $catNum);
		$this->load->view('inv2/match_items', $data);
	}
	
	public function link($userId, $itemId)
	{
		$linkUrl = $this->input->post ( 'linkUrl' );
		// Call python script. Link the inventory item with eBay item url
		$result = $this->call_link_script($userId, $itemId, $linkUrl);
		
		if (isset($result) && isset($result['message'])) {
			$this->session->set_flashdata('falshmsg',
					array('type'=>'error', 'content'=>'Failed to link the item. <br/>Cause: '.$result['message']));
			redirect(site_url("/inv2/details/".$userId.'/'.$itemId), 'refresh');
		} else {
			$this->session->set_flashdata('falshmsg',
					array('type'=>'message', 'content'=>'Item['.$userId.'-'.$itemId.'] is linked. <br/>'.$linkUrl));
			redirect(site_url("/inv2/"), 'refresh');
		}
	}
	
	public function image_orignal($userId, $file_name)
	{
		$orignal_file_path = UPLOAD_BASE_PATH . $userId . DIRECTORY_SEPARATOR . $file_name;
		$this->image($orignal_file_path);
	}
	
	public function image_thumbnail($userId, $file_name)
	{
		$orignal_file_path = UPLOAD_BASE_PATH . $userId . DIRECTORY_SEPARATOR . $file_name;
		if (!file_exists($orignal_file_path)) {
			show_404();
		}
		
		// create floder
		$thumbnail_folder_path = THUMBNAILS_BASE_PATH . $userId;
		if (! file_exists ( $thumbnail_folder_path )) {
			mkdir ( $thumbnail_folder_path, 0777, TRUE );
		}
		
		$thumbnail_file_path = THUMBNAILS_BASE_PATH . $userId . DIRECTORY_SEPARATOR . $file_name;
		if (!file_exists($thumbnail_file_path)) {
			// create thumbnail
			$orig_img = imagecreatefromjpeg($orignal_file_path);
			
			$info = getimagesize($orignal_file_path);
			$width = $info[0];
			$height = $info[1];
			$newWidth = 100;
			$newHeight = ($height / $width) * $newWidth;
			$thumbnail_img = imagecreatetruecolor($newWidth, $newHeight);
			
			imagecopyresampled($thumbnail_img, $orig_img, 0, 0, 0, 0, $newWidth, $newHeight, $width, $height);
			imagejpeg($thumbnail_img, $thumbnail_file_path);
		}

		$this->image($thumbnail_file_path);
	}
	
	public function query_recommendation_info() {
		$input_data = $this->input->post ();
		$item['category'] = 'Electronics, Computers';
		$item['marketPriceMin'] = 100.0;
		$item['marketPriceMax'] = 200.0;
		$item['expectedPrice'] = 120.0;
		$item['salesChannel'] = "eBay";
		$data ['result'] = SUCCESS;
		$data ['data'] = $item;
		echo json_encode ( $item );
	}
	
	private function image($file_path)
	{
		if (!file_exists($file_path)) {
			show_404();
		}
		
		header('Content-Length: '.filesize($file_path)); //<-- sends filesize header
		header('Content-Type: image/jpg'); //<-- send mime-type header
		header('Content-Disposition: inline; filename="'.$file_path.'";'); //<-- sends filename header
		readfile($file_path); //<--reads and outputs the file onto the output buffer
		die(); //<--cleanup
		exit; //and exit
	}
	
	private function call_query_categories_scritp($title)
	{
		$data = array($title);
		$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'query_categories.py';
		$result = shell_exec('python ' . $cmd . ' ' . escapeshellarg(json_encode($data)));
		return $this->get_real_result($result);
	}

	private function call_query_items_script($title, $catNum)
	{
		$data = array($title, $catNum);
		$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'query_matched_items.py';
		$result = shell_exec('python ' . $cmd . ' ' . escapeshellarg(json_encode($data)));
		return $this->get_real_result($result);
	}
	
	private function call_link_script($userId, $itemId, $linkUrl)
	{
		$data = array($userId, $itemId, $linkUrl);
		$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'link_item.py';
		$result = shell_exec('python ' . $cmd . ' ' . escapeshellarg(json_encode($data)));
		return $this->get_real_result($result);
	}
	
	private function get_real_result($result)
	{
		$pos = stripos($result, PYTHON_PLACEHOLD);
		if ($pos) {
			$result = substr($result, $pos + strlen(PYTHON_PLACEHOLD));
			$result = json_decode($result, true);
		}
		return $result;
	}
}

?>
