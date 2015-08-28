<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const DEFAULT_SHARE_USER_ID = 'fd3142d3-167b-48c5-8208-2762e2db2fb2';
const DEFAULT_CATALOGUE_GLOBAL_ID = '1051';

/**
 *
 * @property Item_model $item_model
 * @property Catalogue_model $catalogue_model
 * @property Meta_model $meta_model
 * @property Wordpress_model $wordpress_model
 * @property Activity_model $activity_model
 */
class Item extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'item_model' );
		$this->load->model ( 'catalogue_model' );
		$this->load->model ( 'meta_model' );
		$this->load->model ( 'wordpress_model' );
		$this->load->model ( 'activity_model' );
	}
	/* ---------------- page entry ---------------- */
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'item/test_form', $data );
	}
	public function upload_page() {
		$this->load->helper ( 'form' );
		
		$this->load->view ( 'inv/upload_form', array (
				'error' => ' ' 
		) );
	}
	/**
	 * Return all item's ids belong the user
	 *
	 * @param string $userId
	 *        	User's UUID
	 */
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
	/**
	 * Return all item's last update time
	 *
	 * @param string $userId
	 *        	User's UUID
	 */
	public function get_item_update_times($userId) {
		$item_id_array = array ();
		$items_row = $this->item_model->get_items_by_user_id ( $userId );
		foreach ( $items_row as $item ) {
			$item_id_array [$item ['itemId']] = strtotime ( $item ['recUpdateTime'] );
		}
		
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'item_update_times' => $item_id_array 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Get the item by item UUID
	 *
	 * @param string $itemId
	 *        	Item's UUID
	 */
	public function get_item($itemId) {
		$item = $this->item_model->get_item ( $itemId );
		if ($item) {
			// convert date to timestamp
			foreach ( $item as $field_name => $field_value ) {
				if (endsWith ( $field_name, 'Time' )) {
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
			if (count ( $image_names ) > 0)
				$item ['defaultPhotoName'] = $image_names [0];
			
			$data ['result'] = SUCCESS;
			$data ['data'] = array (
					'item' => $item 
			);
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Can not find the item: ' . $itemId;
		}
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function get_item_by_global_id($global_item_id) {
		$item = $this->item_model->get_item_by_global_id ( $global_item_id );
		if ($item) {
			// convert date to timestamp
			foreach ( $item as $field_name => $field_value ) {
				if (endsWith ( $field_name, 'Time' )) {
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
			if (count ( $image_names ) > 0)
				$item ['defaultPhotoName'] = $image_names [0];
			
			$data ['result'] = SUCCESS;
			$data ['data'] = array (
					'item' => $item 
			);
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Can not find the item: ' . $global_item_id;
		}
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Get the item all details for browse
	 *
	 * @param string $item_id        	
	 */
	public function browse_item($item_id) {
		$item = $this->item_model->get_item ( $item_id );
		if (! $item) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Can not find the requested item';
			return;
		}
		
		// convert date to timestamp
		foreach ( $item as $field_name => $field_value ) {
			if (endsWith ( $field_name, 'Time' )) {
				$field_value = strtotime ( $field_value );
				$item [$field_name] = $field_value;
			}
		}
		// image names
		$images_row = $this->item_model->get_images ( $item ['Global_Item_ID'] );
		$images = array ();
		foreach ( $images_row as $image_row )
			array_push ( $images, $image_row ['imageName'] );
		
		$this->load->model ( 'user_model' );
		$user = $this->user_model->get_user ( $item ['userId'] );
		$user ['password'] = '';
		
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'item' => $item,
				'images' => $images,
				'user' => $user 
		);
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Query the items.
	 *
	 * @param string $key_word        	
	 * @param integer $limit        	
	 * @param integer $offset        	
	 */
	public function query_items() {
		$key_word = $this->input->post ( 'key_word' );
		if ($key_word) {
			$key_word_where = "(item.title LIKE '%${key_word}%' OR item.desc LIKE '%${key_word}%')";
			$where [$key_word_where] = NULL;
		}
		$category = $this->input->post ( 'category' );
		if ($category) {
			$where ['category'] = $category;
		}
		$availability = $this->input->post ( 'availability' );
		if ($availability) {
			$where ['availability'] = $availability;
		} else {
			$where ['(availability = \'AB\' OR availability = \'SD\')'] = NULL;
		}
		if ($radius = $this->input->post ( 'radius' )) {
			$this->load->helper ( 'location' );
			$latitude = $this->input->post ( 'latitude' );
			$longitude = $this->input->post ( 'longitude' );
			if (! $latitude || ! $longitude) {
				$loc = get_loc_by_zipcode ( $this->input->post ( 'user_zip_code' ) );
				if ($loc) {
					$latitude = $loc ['latitude'];
					$longitude = $loc ['longitude'];
				}
			}
			$range = calculate_latitude_longitude_range ( $latitude, $longitude, $radius );
			$where ['latitude > '] = $range ['latitude_min'];
			$where ['latitude < '] = $range ['latitude_max'];
			$where ['longitude > '] = $range ['longitude_min'];
			$where ['longitude < '] = $range ['longitude_max'];
		}
		$limit = $this->input->post ( 'limit' ) ? $this->input->post ( 'limit' ) : 5;
		$offset = $this->input->post ( 'offset' ) ? $this->input->post ( 'offset' ) : 0;
		$items = $this->item_model->query_items ( $where, $limit, $offset );
		$count = $this->item_model->count_items ( $where );
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'count' => $count,
				'items' => $items 
		);
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	
	/**
	 * Update the item from the post data.
	 */
	public function update_item() {
		$input_data = $this->get_input_data ();
		$loc = $this->get_location ( $input_data );
		if ($loc) {
			$input_data = array_merge ( $input_data, $loc );
		}
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
			$data ['message'] = 'Internal Error: Failed to update the database.';
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		
		$data ['result'] = SUCCESS;
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Mark the status of the item as 'XX' and the item will not be find in the query API.
	 *
	 * @param string $itemId
	 *        	Item's UUID
	 */
	public function delete_item($itemId) {
		$item = $this->item_model->get_item ( $itemId );
		if ($item) {
			$result = $this->item_model->update_item ( array (
					'itemId' => $itemId,
					'availability' => 'XX' 
			) );
			if ($result) {
				$this->item_model->insert_item_history ( $item );
				$data ['result'] = SUCCESS;
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = 'Internal Error: Failed to update the database.';
			}
		} else {
			// May be the item didn't be upload to the server. It's OK to return SUCCESS.
			$data ['result'] = SUCCESS;
		}
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Get the item's all image names.
	 *
	 * @param string $itemId
	 *        	Item's UUID
	 */
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
	function upload() {
		$userId = $this->input->post ( 'userId' );
		log_message ( 'debug', 'upload image: userid=' . $userId );
		
		$upload_path = UPLOAD_BASE_PATH . $userId;
		if (! file_exists ( $upload_path )) {
			mkdir ( $upload_path, 0777, true );
		}
		
		$config ['upload_path'] = $upload_path;
		$config ['allowed_types'] = '*';
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
				"latitude" => "latitude",
				"longitude" => "longitude",
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
				if (endsWith ( $field_name, 'Time' )) {
					$field_value = date ( 'Y-m-d H:i:s', $field_value );
				}
				$input_data [$field_name] = $field_value;
			}
		}
		return $input_data;
	}
	private function gen_uuid() {
		return sprintf ( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x', 
				// 32 bits for "time_low"
				mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), 
				
				// 16 bits for "time_mid"
				mt_rand ( 0, 0xffff ), 
				
				// 16 bits for "time_hi_and_version",
				// four most significant bits holds version number 4
				mt_rand ( 0, 0x0fff ) | 0x4000, 
				
				// 16 bits, 8 bits for "clk_seq_hi_res",
				// 8 bits for "clk_seq_low",
				// two most significant bits holds zero and one for variant DCE1.1
				mt_rand ( 0, 0x3fff ) | 0x8000, 
				
				// 48 bits for "node"
				mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ) );
	}
	private function get_location($input_data) {
		$this->load->helper ( 'location' );
		$loc = NULL;
		if ($input_data ['latitude']) {
			$loc = get_loc_by_latlng ( $input_data ['latitude'], $input_data ['longitude'] );
			if ($loc)
				return array (
						'region' => build_region_string_by_loc ( $loc ) 
				);
		} else {
			$this->load->model ( 'user_model' );
			$user = $this->user_model->get_user ( $input_data ['userId'] );
			if (! empty ( $user ['zipcode'] )) {
				$loc = get_loc_by_zipcode ( $user ['zipcode'] );
				if ($loc)
					return array (
							'latitude' => $loc ['latitude'],
							'longitude' => $loc ['longitude'],
							'region' => build_region_string_by_loc ( $loc ) 
					);
			}
		}
		return $loc;
	}
}

?>
