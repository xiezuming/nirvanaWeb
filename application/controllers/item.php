<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;
const UPLOAD_BASE_PATH = '/var/uploads/wetag_app/';
const LOG_BASE_PATH = '/var/log/wetag/';

/**
 *
 * @property Item_model $item_model
 * @property Catalogue_model $catalogue_model
 * @property Meta_model $meta_model
 * @property Wordpress_model $wordpress_model
 */
class Item extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'item_model' );
		$this->load->model ( 'catalogue_model' );
		$this->load->model ( 'meta_model' );
		$this->load->model ( 'wordpress_model' );
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'item/test_form', $data );
	}
	public function get_item_ids($userId) {
		$item_id_array = array ();
		$items_row = $this->item_model->get_items_by_user_id ( $userId );
		foreach ( $items_row as $item ) {
			array_push ( $item_id_array, $item ['itemId'] );
		}
		
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'item_ids' => $item_id_array 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function get_item($itemId) {
		$item = $this->item_model->get_item ( $itemId );
		if ($item) {
			// convert date to timestamp
			foreach ( $item as $field_name => $field_value ) {
				if ($this->endsWith ( $field_name, 'Time' )) {
					$field_value = strtotime ( $field_value );
					$item [$field_name] = $field_value;
				}
			}
			// image names
			$images = $this->item_model->get_images ( $item ['Global_Item_ID'] );
			$image_names = array ();
			foreach ( $images as $image )
				array_push ( $image_names, $image ['imageName'] );
			$item ['photoNames'] = implode ( ";", $image_names );
			if (count($image_names) > 0)
				$item['defaultPhotoName'] = $image_names[0];
			
			$data ['result'] = SUCCESS;
			$data ['data'] = array (
					'item' => $item 
			);
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Can not find the item: ' . $itemId;
		}
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function update_item() {
		$input_data = $this->get_input_data ();
		$input_data ['synchWp'] = 'N';
		$itemId = $input_data ['itemId'];
		
		$photoNames = $this->input->post ( 'photoNames' );
		$newImageNameArray = empty ( $photoNames ) ? array () : explode ( ";", $photoNames );
		sort ( $newImageNameArray );
		$oldImageNameArray = array ();
		
		$this->db->trans_start ();
		
		$oldItem = $this->item_model->get_item ( $itemId );
		if ($oldItem) {
			// build old image name array
			$globalItemId = $oldItem ['Global_Item_ID'];
			$oldImageRowArray = $this->item_model->get_images ( $globalItemId );
			foreach ( $oldImageRowArray as $oldImageRow ) {
				array_push ( $oldImageNameArray, $oldImageRow ['imageName'] );
			}
			$oldItem ['photoNames'] = implode ( ";", $oldImageNameArray );
			
			// insert the item old row into the item history table
			$this->item_model->insert_item_history ( $oldItem );
			
			$this->item_model->update_item ( $input_data );
			$item = $this->item_model->get_item ( $itemId );
		} else {
			$this->item_model->insert_item ( $input_data );
			$item = $this->item_model->get_item ( $itemId );
			$globalItemId = $item ['Global_Item_ID'];
			
			// add the new item into the user default catalogue
			// $this->catalogue_model->insert_user_default_catalogue_item_relation ( $item );
		}
		
		// update image names
		$insertImageNameArray = array_diff ( $newImageNameArray, $oldImageNameArray );
		$deleteImageNameArray = array_diff ( $oldImageNameArray, $newImageNameArray );
		foreach ( $insertImageNameArray as $insertImageName )
			$this->item_model->insert_image ( $globalItemId, $insertImageName );
		foreach ( $deleteImageNameArray as $deleteImageName )
			$this->item_model->delete_image ( $globalItemId, $deleteImageName );
		
		$this->db->trans_complete ();
		
		if ($this->db->trans_status () === FALSE) {
			log_message ( 'error', 'Item.update_item: Failed to update the database.' );
			$data ['result'] = FAILURE;
			$data ['message'] = 'Failed to update the database.';
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		
		// synchronize to wp database
		$success = $this->synch_item ( $globalItemId );
		if ($success) {
			$this->item_model->update_item ( array (
					'itemId' => $itemId,
					'synchWp' => 'Y' 
			) );
		}
		
		// call python script to resize and upload image files
		$global_image_id_array = array ();
		$image_row_array = $this->item_model->get_images ( $globalItemId );
		foreach ( $image_row_array as $image_row ) {
			if ($image_row ['synchWp'] == 'N')
				array_push ( $global_image_id_array, $image_row ['Global_Item_Image_ID'] );
		}
		if (count ( $global_image_id_array ) > 0)
			$this->exec_image_generator_script ( $global_image_id_array );
		
		$data ['result'] = SUCCESS;
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function get_item_image_names($itemId) {
		if (empty ( $itemId )) {
			echo 'ERROR: itemId is empty.';
			return;
		}
		$image_name_array = array ();
		$item = $this->item_model->get_item ( $itemId );
		if ($item) {
			$image_row_array = $this->item_model->get_images ( $item ['Global_Item_ID'] );
			foreach ( $image_row_array as $image_row )
				array_push ( $image_name_array, $image_row ['imageName'] );
		}
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'image_names' => $image_name_array 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function test_synch_item() {
		$global_item_id = $this->input->post ( 'global_item_id' );
		if (empty ( $global_item_id )) {
			echo 'ERROR: global_item_id is empty.';
			return;
		}
		echo 'Restult: ' . var_export ( $this->synch_item ( $global_item_id ), TRUE );
	}
	
	/**
	 * Synch the item information to WordPress database
	 *
	 * @param $global_item_id: Global_Item_ID        	
	 * @return boolean Returns TRUE if success.
	 */
	private function synch_item($global_item_id) {
		log_message ( 'debug', 'Start to synchronize the item to WordPress DB.' );
		
		$item = $this->item_model->get_item_by_global_id ( $global_item_id );
		if (! $item) {
			log_message ( 'error', 'Item.synch_item: Can not find the item.' . $global_item_id );
			return FALSE;
		}
		
		// build data
		$first_image_row = $this->item_model->get_first_image ( $global_item_id );
		$item_photo_url = '';
		if ($first_image_row && strlen ( $first_image_row ['imageName'] ) > 4) {
			$item_photo_url = 'http://happitail.info/wetagimg/' . $item ['userId'] . '/' . $first_image_row ['imageName'];
			$postfix = $item ['availability'] == 'AB' ? '-360' : '-360sold';
			$item_photo_url = substr_replace ( $item_photo_url, $postfix, - 4, 0 );
		}
		$condition_row = $this->meta_model->get_meta_code ( 2, $item ['condition'] );
		$desc_prefix = $condition_row ? 'Condition: ' . $condition_row ['value'] . '.' : '';
		$category_row = $this->meta_model->get_meta_code ( 1, $item ['category'] );
		$catagory_id = $category_row ? $category_row ['pos'] : - 1;
		$catagory_name = $category_row ? $category_row ['value'] : '';
		$wp_item_data = array (
				'Item_ID' => $global_item_id,
				'Item_Name' => $item ['title'],
				'Item_Slug' => '',
				'Item_Description' => $desc_prefix . $item ['desc'],
				'Item_Price' => '$' . $item ['expectedPrice'],
				'Item_Photo_URL' => $item_photo_url,
				'Category_ID' => $catagory_id,
				'Category_Name' => $catagory_name,
				'Item_Date_Created' => $item ['recCreateTime'],
				'Item_Display_Status' => 'Show' 
		);
		$newImageRowArray = $this->item_model->get_images ( $global_item_id );
		
		$wp_db = $this->load->database ( 'wp', TRUE );
		if (! $wp_db->initialize ()) {
			log_message ( 'error', 'Item.synch_item: Failed to connect the database.' );
			return FALSE;
		}
		
		$this->wordpress_model->db = $wp_db;
		$wp_db->trans_start ();
		
		// update WordPress item table
		if ($this->wordpress_model->get_item ( $global_item_id )) {
			$success = $this->wordpress_model->update_item ( $wp_item_data );
			if ($success)
				$success = $this->wordpress_model->delete_images ( $global_item_id );
		} else {
			$success = $this->wordpress_model->insert_item ( $wp_item_data );
		}
		if ($success) {
			// update WordPress item image table
			foreach ( $newImageRowArray as $newImageRow ) {
				$item_image_id = $newImageRow ['Global_Item_Image_ID'];
				$item_image_url = 'http://happitail.info/wetagimg/' . $item ['userId'] . '/' . $newImageRow ['imageName'];
				$item_image_url = substr_replace ( $item_image_url, '-800', - 4, 0 );
				$success = $this->wordpress_model->insert_image ( $item_image_id, $global_item_id, $item_image_url );
				if (! $success)
					break;
			}
		}
		
		$wp_db->trans_complete ();
		
		if ($wp_db->trans_status () === FALSE) {
			log_message ( 'error', 'Item.synch_item: Failed to update the database.' );
			return FALSE;
		} else {
			log_message ( 'debug', 'Item.synch_item: Synchronize to WordPress database successfully.' );
			return TRUE;
		}
		return TRUE;
	}
	public function test_image_generator() {
		$global_image_ids = $this->input->post ( 'global_image_ids' );
		$wait_until_done = $this->input->post ( 'wait_until_done' );
		if (empty ( $global_image_ids )) {
			echo 'ERROR: global_image_ids is empty.';
			return;
		}
		echo 'Restult: <pre>' . $this->exec_image_generator_script ( explode ( ";", $global_image_ids ), $wait_until_done ) . '</pre>';
	}
	/**
	 * Call image generator script to resize & upload the image files.
	 *
	 * @param array $global_image_id_array        	
	 * @param boolean $wait_until_done        	
	 * @return The shell result if $wait_until_done = TRUE
	 */
	private function exec_image_generator_script($global_image_id_array, $wait_until_done = FALSE) {
		$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'imageGenerator.py' . ' ' . escapeshellarg ( json_encode ( $global_image_id_array ) );
		if (! $wait_until_done) {
			$log_file = LOG_BASE_PATH . 'imageGenerator-' . date ( 'Y-m-d' ) . '.log';
			$cmd = $cmd . ' >> ' . $log_file . ' 2>>' . $log_file . ' &';
		}
		log_message ( 'debug', $cmd );
		
		$result = shell_exec ( 'python ' . $cmd );
		if ($wait_until_done)
			return $result;
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
				"priceGroup" => "priceGroup",
				"catNum" => "catNum",
				"similarItemUrl" => "similarItemUrl",
				"recCreateTime" => "recCreateTime",
				"recUpdateTime" => "recUpdateTime" 
		);
		return $field_names;
	}
	private function get_input_data() {
		log_message ( 'debug', 'input: ' . print_r ( $this->input->post (), TRUE ) );
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
	private function map_item_to_wpitem($item) {
	}
	private function endsWith($haystack, $needle) {
		return $needle === "" || substr ( $haystack, - strlen ( $needle ) ) === $needle;
	}
}

?>
