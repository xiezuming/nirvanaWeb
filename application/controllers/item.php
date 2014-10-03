<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const UPLOAD_BASE_PATH = '/var/uploads/wetag_app/';
const DEFAULT_SHARE_USER_ID = 'fd3142d3-167b-48c5-8208-2762e2db2fb2';
const DEFAULT_CATALOGUE_GLOBAL_ID = '1051';

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
			if (count ( $image_names ) > 0)
				$item ['defaultPhotoName'] = $image_names [0];
			
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
	/**
	 * Query the items.
	 *
	 * @param string $key_word        	
	 * @param integer $limit        	
	 * @param integer $offset        	
	 */
	public function query_items() {
		$where ['availability'] = 'AB';
		$key_word = $this->input->post ( 'key_word' );
		if ($key_word) {
			$key_word_where = "(LOWER(item.title) LIKE '%" . strtolower ( $key_word ) . "%'
					OR LOWER(item.desc) LIKE '%" . strtolower ( $key_word ) . "%')";
			$where [$key_word_where] = NULL;
		}
		$category = $this->input->post ( 'category' );
		if ($category) {
			$where ['category'] = $category;
		}
		$group = $this->input->post ( 'group_key' );
		if ($group) {
			$where ['group_key'] = $group;
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
	 * 1. Insert or Update the item into the DB.
	 * 2. Sync the item to the WordPress's DB.
	 * 3. Start a asynchronous process to resize & upload the images to the WordPress server.
	 */
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
		$this->synch_item ( $globalItemId );
		
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
				$data ['message'] = 'Failed to update the database.';
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
	public function test_synch_item() {
		$global_item_id = $this->input->post ( 'global_item_id' );
		if (empty ( $global_item_id )) {
			echo 'ERROR: global_item_id is empty.';
			return;
		}
		echo 'Restult: ' . var_export ( $this->synch_item ( $global_item_id ), TRUE );
	}
	public function sync_all_items() {
		$items = $this->item_model->query_all_items ( "synchWp = 'N'" );
		$success_count = 0;
		$failure_count = 0;
		$failure_array = array ();
		foreach ( $items as $item ) {
			$global_item_id = $item ['Global_Item_ID'];
			log_message ( 'debug', 'sync_all_items: ' . $global_item_id . '...' );
			$success = $this->synch_item ( $global_item_id );
			if ($success) {
				$success_count ++;
			} else {
				$failure_count ++;
				array_push ( $failure_array, $global_item_id );
			}
			log_message ( 'debug', 'Restult: ' . $global_item_id . var_export ( $success, TRUE ) );
		}
		$data ['success_count'] = $success_count;
		$data ['failure_count'] = $failure_count;
		$data ['failure_array'] = $failure_array;
		$data ['result'] = $failure_count ? FAILURE : SUCCESS;
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function sync_all_images() {
		$images = $this->item_model->query_all_images ( "synchWp = 'N'" );
		$image_count = count ( $images );
		$global_image_id_array = array ();
		foreach ( $images as $image ) {
			array_push ( $global_image_id_array, $image ['Global_Item_Image_ID'] );
		}
		$wait_until_done = TRUE;
		$this->exec_image_generator_script ( $global_image_id_array, $wait_until_done );
		
		$images = $this->item_model->query_all_images ( "synchWp = 'N'" );
		$global_image_id_array = array ();
		foreach ( $images as $image ) {
			array_push ( $global_image_id_array, $image ['Global_Item_Image_ID'] );
		}
		$current_image_count = count ( $images );
		$data ['success_count'] = $image_count - $current_image_count;
		$data ['failure_count'] = $current_image_count;
		$data ['failure_array'] = $global_image_id_array;
		$data ['result'] = $current_image_count ? FAILURE : SUCCESS;
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Synch the item information to WordPress database
	 *
	 * @param string $global_item_id:
	 *        	Item's global ID
	 * @return boolean Returns TRUE if success.
	 */
	public function synch_item($global_item_id) {
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
		$keyword = empty ( $item ['barcode'] ) ? $item ['title'] : $item ['barcode'];
		$amazon_link = 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&tag=happitailcom-20&field-keywords=' . urlencode ( $keyword );
		$amazon_link = '<br/><a href="' . htmlspecialchars ( $amazon_link ) . '">View Similar items on Amazon</a>';
		$wp_item_data = array (
				'Item_ID' => $global_item_id,
				'Item_Name' => $item ['title'],
				'Item_Slug' => '',
				'Item_Description' => $desc_prefix . '<br/>' . str_replace ( "\n", '<br/>', $item ['desc'] ) . $amazon_link,
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
			$this->item_model->update_item ( array (
					'itemId' => $item ['itemId'],
					'synchWp' => 'Y' 
			) );
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
	function upload_item_web() {
		$data ['title'] = 'Upload';
		$data ['error'] = '';
		
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		$this->form_validation->set_rules ( 'email', 'Email Address', 'required||max_length[45]|valid_email' );
		$this->form_validation->set_rules ( 'title', 'Title', 'required' );
		$this->form_validation->set_rules ( 'price', 'Price', 'required|integer' );
		$this->form_validation->set_rules ( 'description', 'Description', 'required' );
		$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', '' );
		
		if ($this->form_validation->run ()) {
			// upload image file
			$upload_path = UPLOAD_BASE_PATH . DEFAULT_SHARE_USER_ID;
			if (! file_exists ( $upload_path )) {
				mkdir ( $upload_path, 0777, true );
			}
			
			$image_name = time () . '.jpg';
			$config ['upload_path'] = $upload_path;
			$config ['allowed_types'] = 'gif|jpg|png';
			$config ['max_size'] = '5120';
			$config ['overwrite'] = TRUE;
			$config ['file_name'] = $image_name;
			
			$this->load->library ( 'upload', $config );
			if ($this->upload->do_upload ()) {
				$itemId = $this->gen_uuid ();
				$date_now = date ( 'Y-m-d H:i:s' );
				$description = $this->input->post ( 'description' );
				$description .= 'Email: ' . $this->input->post ( 'email' ) . "<br/>";
				if ($this->input->post ( 'wechatId' ))
					$description .= 'WeChat ID: ' . $this->input->post ( 'wechatId' ) . "<br/>";
				
				$input_data ['itemId'] = $itemId;
				$input_data ['userId'] = DEFAULT_SHARE_USER_ID;
				$input_data ['title'] = $this->input->post ( 'title' );
				$input_data ['category'] = 'CLO';
				$input_data ['expectedPrice'] = $this->input->post ( 'price' );
				$input_data ['condition'] = 'GD';
				$input_data ['availability'] = 'AB';
				$input_data ['desc'] = $description;
				$input_data ['recCreateTime'] = $date_now;
				$input_data ['recUpdateTime'] = $date_now;
				$input_data ['synchWp'] = 'N';
				
				$this->db->trans_start ();
				
				// insert the itme into item table
				$this->item_model->insert_item ( $input_data );
				$item = $this->item_model->get_item ( $itemId );
				$globalItemId = $item ['Global_Item_ID'];
				
				// add the new item into the user default catalogue
				$this->catalogue_model->insert_user_default_catalogue_item_relation ( DEFAULT_CATALOGUE_GLOBAL_ID, $globalItemId );
				
				// insert image names into item_image table
				$this->item_model->insert_image ( $globalItemId, $image_name );
				
				$this->db->trans_complete ();
				
				if ($this->db->trans_status () === FALSE) {
					log_message ( 'error', 'Item.upload: Failed to update the database.' );
					$data ['error'] = 'Failed to update the database.';
					$this->load->view ( 'share/upload_form', $data );
					return;
				}
				// synchronize to wp database
				$this->synch_item ( $globalItemId );
				$this->synch_catalogue ( DEFAULT_CATALOGUE_GLOBAL_ID );
				
				// call python script to resize and upload image files
				$global_image_id_array = array ();
				$image_row_array = $this->item_model->get_images ( $globalItemId );
				foreach ( $image_row_array as $image_row ) {
					if ($image_row ['synchWp'] == 'N')
						array_push ( $global_image_id_array, $image_row ['Global_Item_Image_ID'] );
				}
				if (count ( $global_image_id_array ) > 0)
					$this->exec_image_generator_script ( $global_image_id_array );
				
				$this->load->view ( 'share/upload_success', $data );
				return;
			} else {
				$data ['error'] = $this->upload->display_errors ();
				$this->load->view ( 'share/upload_form', $data );
				return;
			}
		}
		$this->load->view ( 'share/upload_form', $data );
	}
	/**
	 * Synchronize the catalogue and its relations information to WordPress database
	 *
	 * @param $global_catalogue_id: Global_Catalogue_ID        	
	 * @return boolean Returns TRUE if success.
	 */
	private function synch_catalogue($global_catalogue_id) {
		log_message ( 'debug', 'Start to synchronize the catalogue to WordPress DB.' );
		
		$catalogue = $this->catalogue_model->get_catalogue_by_global_id ( $global_catalogue_id );
		if (! $catalogue) {
			log_message ( 'error', 'Catalogue.synch_catalogue: Can not find the catalogue.' . $global_catalogue_id );
			return FALSE;
		}
		
		// build data
		$wp_catalogue_data = array (
				'Catalogue_ID' => $global_catalogue_id,
				'Catalogue_Name' => $catalogue ['catalogueName'],
				'Catalogue_Description' => '',
				'Catalogue_Layout_Format' => '',
				'Catalogue_Custom_CSS' => '',
				'Catalogue_Date_Created' => $catalogue ['recCreateTime'] 
		);
		$newRelationArray = $this->catalogue_model->get_catalogue_item_relations ( $global_catalogue_id );
		
		$wp_db = $this->load->database ( 'wp', TRUE );
		if (! $wp_db->initialize ()) {
			log_message ( 'error', 'Catalogue.synch_catalogue: Failed to connect the database.' );
			return FALSE;
		}
		
		$this->wordpress_model->db = $wp_db;
		$wp_db->trans_start ();
		
		// update WordPress catalgoue table
		if ($this->wordpress_model->get_catalogue ( $global_catalogue_id )) {
			$success = $this->wordpress_model->update_catalogue ( $wp_catalogue_data );
			if ($success)
				$success = $this->wordpress_model->delete_catalogue_all_relations ( $global_catalogue_id );
		} else {
			$success = $this->wordpress_model->insert_catalogue ( $wp_catalogue_data );
		}
		if ($success) {
			// update WordPress catalogue item relation table
			// TODO current sort the item order by their global itme id. Need think about it.
			$position = 0;
			foreach ( $newRelationArray as $newRelation ) {
				$success = $this->wordpress_model->delete_catalogue_item_relation ( $newRelation ['Global_Catalogue_Item_ID'] );
				if (! $success)
					break;
				$success = $this->wordpress_model->insert_catalogue_item_relation ( $newRelation ['Global_Catalogue_Item_ID'], $newRelation ['Global_Catalogue_ID'], $newRelation ['Global_Item_ID'], $position );
				if (! $success)
					break;
				$position ++;
			}
		}
		
		$wp_db->trans_complete ();
		
		if ($wp_db->trans_status () === FALSE) {
			log_message ( 'error', 'Catalogue.synch_catalogue: Failed to update the WordPresss database.' );
			return FALSE;
		} else {
			log_message ( 'debug', 'Catalogue.synch_catalogue: Synchronize to WordPress database successfully.' );
			$this->catalogue_model->update_catalogue ( array (
					'catalogueId' => $catalogue ['catalogueId'],
					'synchWp' => 'Y' 
			) );
			return TRUE;
		}
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
}

?>
