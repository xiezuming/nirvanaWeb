<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;
const UPLOAD_BASE_PATH = '/var/uploads/wetag_app/';

/**
 *
 * @property Item_model $item_model
 * @property User_model $user_model
 */
class Item extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'item_model' );
		$this->load->model ( 'user_model' );
		$this->load->model ( 'inv_recommendation_model' );
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'item/test_form', $data );
	}
	public function update_item() {
		$input_data = $this->get_input_data ();
		$input_data['synchWp'] = 'N';
		$itemId = $input_data ['itemId'];
		
		log_message ( 'debug', 'update_item: $itemId = ' . $itemId );
		
		$this->db->trans_start ();
		
		$item = $this->item_model->get_item ( $itemId );
		if ($item) {
			// deletel photos files.
			$path = UPLOAD_BASE_PATH . $item ['userId'] . '/';
			$photoNames = array ();
			foreach ( $this->item_model->get_photos ( $itemId ) as $photo ) {
				$photoName = $photo ['photoName'];
				$this->delete_file ( $path . $photoName );
				array_push ( $photoNames, $photoName );
			}
			$this->item_model->delete_photos ( $itemId );
			
			$item ['photoNames'] = implode ( ";", $photoNames );
			unset($item['synchWp']);
			
			$this->item_model->insert_item_history ( $item );
			$this->item_model->update_item ( $input_data );
		} else {
			$this->item_model->insert_item ( $input_data );
		}
		// insert photo names
		$photoNames = $this->input->post ( 'photoNames' );
		if (! empty ( $photoNames )) {
			foreach ( explode ( ";", $photoNames ) as $photoName ) {
				$this->item_model->insert_photo ( $itemId, $photoName );
			}
		}
		
		$this->db->trans_complete ();
		if ($this->db->trans_status() === FALSE)
		{
			log_message('error', 'Failed to update the database.');
			$data ['result'] = FAILURE;
			$data ['message'] = 'Failed to update the database.';
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		// synchronize to wp database
		
		$this->db = $this->load->database('wp', TRUE);
		$this->db->insert( 'wp_UPCP_Items', $input_data );
		if (mysql_errno() !== 0) {
			log_message('error', 'Failed to synchronize the item to WP database. ' . mysql_error());
		}
		
		$data ['result'] = SUCCESS;
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	private function delete_file($file_path) {
		if (file_exists ( $file_path )) {
			unlink ( $file_path );
		}
	}
	function upload() {
		$userId = $this->input->post ( 'userId' );
		$upload_path = UPLOAD_BASE_PATH . $userId;
		if (! file_exists ( $upload_path )) {
			mkdir ( $upload_path, 0777, true );
		}
		
		$config ['upload_path'] = $upload_path;
		$config ['allowed_types'] = 'gif|jpg|png';
		$config ['max_size'] = '5120';
		$config ['overwrite'] = TRUE;
		
		$this->load->library ( 'upload', $config );
		if ($this->upload->do_upload ()) {
			$data ['result'] = SUCCESS;
			$data ['data'] = $this->upload->data ();
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = $this->upload->display_errors ();
		}
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function upload_page() {
		$this->load->helper ( 'form' );
		
		$this->load->view ( 'inv/upload_form', array (
				'error' => ' ' 
		) );
	}
	private function get_field_names() {
		$field_names = array (
				"itemId" => "itemId",
				"userId" => "userId",
				"title" => "title",
				"barcode" => "barcode",
				"category" => "category",
				"marketPriceMin" => "marketPriceMin",
				"marketPriceMax" => "marketPriceMax",
				"expectedPrice" => "expectedPrice",
				"condition" => "condition",
				"salesChannel" => "salesChannel",
				"availability" => "availability",
				"desc" => "desc",
				"recCreateTime" => "recCreateTime",
				"recUpdateTime" => "recUpdateTime" 
		);
		return $field_names;
	}
	private function get_input_data() {
		$input_data = array ();
		foreach ( $this->get_field_names () as $field_name ) {
			$field_value = $this->input->post ( $field_name );
			if (empty ( $field_value )) {
				$input_data [$field_name] = NULL;
			} else {
				// change
				if ($this->endsWith ( $field_name, 'Time' )) {
					$field_value = date ( 'Y-m-d H:i:s', $field_value );
				}
				$input_data [$field_name] = $field_value;
			}
		}
		return $input_data;
	}
	
	private function map_item_to_wpitem($item){
	}
	private function endsWith($haystack, $needle) {
		return $needle === "" || substr ( $haystack, - strlen ( $needle ) ) === $needle;
	}
}

?>
