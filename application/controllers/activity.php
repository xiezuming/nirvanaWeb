<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

/**
 *
 * @property Item_model $item_model
 * @property Activity_model $activity_model
 * @property User_model $user_model
 * @property Meta_model $meta_model
 * @property Wordpress_model $wordpress_model
 */
class Activity extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'item_model' );
		$this->load->model ( 'activity_model' );
		$this->load->model ( 'user_model' );
		$this->load->model ( 'meta_model' );
		$this->load->model ( 'wordpress_model' );
	}
	/* ---------------- page entry ---------------- */
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['title'] = 'TEST';
		$this->load->view ( 'templates/web_header', $data );
		$this->load->view ( 'activity/test_form', $data );
		$this->load->view ( 'templates/web_footer', $data );
	}
	function get_item_b64UUID() {
		$itemId = $this->input->post ( 'itemId' );
		$global_item_id = $this->input->post ( 'global_item_id' );
		if (! empty ( $itemId )) {
			$item = $this->item_model->get_item ( $itemId );
		} else if (! empty ( $global_item_id )) {
			$item = $this->item_model->get_item_by_global_id ( $global_item_id );
		} else {
			show_404 ();
		}
		
		$this->load->helper ( 'uuid' );
		echo "item_id: ${item['Global_Item_ID']}<br/>";
		echo "item_id: ${item['itemId']}<br/>";
		echo "b64_item_id: " . encode_uuid_base64 ( $item ['itemId'] );
	}
	function add_item($activity_id) {
		$activity = $this->activity_model->get_activity ( $activity_id );
		if (! $activity) {
			show_404 ();
			return;
		}
		
		$data ['title'] = 'Submit Item - ' . $activity ['Activity_Name'];
		$data ['activity'] = $activity;
		
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		$this->form_validation->set_rules ( 'email', 'Email Address', 'required||max_length[45]|valid_email' );
		$this->form_validation->set_rules ( 'title', 'Title', 'required' );
		$this->form_validation->set_rules ( 'price', 'Price', 'required|numeric' );
		$this->form_validation->set_rules ( 'condition', 'Condition', 'required' );
		$this->form_validation->set_rules ( 'description', 'Description', 'required' );
		$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', '' );
		$this->form_validation->set_rules ( 'zipcode', 'ZIP Code', 'required' );
		
		if (! $this->form_validation->run ()) {
			$data ['error'] = '';
			return $this->load_add_item_view ( $data );
		}
		
		// get the user by email. create it if not exist.
		$user = $this->create_user ();
		if (! $user) {
			$data ['error'] = 'Internal Error: failed to create the user.';
			return $this->load_add_item_view ( $data );
		}
		
		// save the image file to server folder
		$image_names = $this->save_uploaded_image ( $user ['userId'] );
		if (count ( $image_names ) == 0) {
			$data ['error'] = 'Please choose the picture.';
			return $this->load_add_item_view ( $data );
		}
		
		// save the item into the DB
		$item = $this->save_item ( $user ['userId'], $image_names );
		if (! $item) {
			log_message ( 'error', 'Activity.save_item: Failed to update the database.' );
			$data ['error'] = 'Failed to update the database.';
			return $this->load_add_item_view ( $data );
		}
		$global_item_id = $item ['Global_Item_ID'];
		
		// synchronize to wp database
		$result = $this->sync_item_to_wordpress ( $global_item_id, $user ['userId'] );
		if (! $result) {
			$data ['error'] = 'Failed to update the WordPress database.';
			return $this->load_add_item_view ( $data );
		}
		
		// call python script to resize and upload image files
		resize_upload_images ( $global_item_id, $this->item_model );
		
		// send the email
		$this->send_item_success_email ( $item, $user ['email'], $activity_id );
		
		$data ['title'] = 'Success - Submit Your Item';
		$this->load->view ( 'templates/web_header', $data );
		$this->load->view ( 'activity/add_item_success', $data );
		$this->load->view ( 'templates/web_footer', $data );
	}
	private function load_add_item_view($data) {
		$data ['meta_condition'] = $this->meta_model->get_meta_code_array ( META_TYPE_CONDITION );
		
		$this->load->view ( 'templates/web_header', $data );
		$this->load->view ( 'activity/add_item', $data );
		$this->load->view ( 'templates/web_footer', $data );
	}
	private function create_user() {
		$email = $this->input->post ( 'email' );
		$user = $this->user_model->query_user ( array (
				'email' => $email,
				'userType' => USER_TYPE_WETAG 
		) );
		if (! $user) {
			$user_id = $this->user_model->create_user ( array (
					'userType' => USER_TYPE_WETAG,
					'alias' => '',
					'firstName' => '',
					'lastName' => '',
					'email' => $email,
					'wechatId' => $this->input->post ( 'wechatId' ),
					'zipcode' => $this->input->post ( 'zipcode' ) 
			) );
			if ($user_id) {
				$user = $this->user_model->get_user ( $user_id );
			}
		}
		return $user;
	}
	private function save_uploaded_image($user_id) {
		$upload_path = UPLOAD_BASE_PATH . $user_id;
		if (! file_exists ( $upload_path )) {
			mkdir ( $upload_path, 0777, true );
		}
		
		$image_names = array ();
		$base_time = time ();
		$images_data = $this->input->post ( 'image_data' );
		if ($images_data) {
			foreach ( $images_data as $image_data ) {
				if ($image_data) {
					$image_data = str_replace ( 'data:image/jpeg;base64,', '', $image_data );
					$image_data = str_replace ( ' ', '+', $image_data );
					$image_data = base64_decode ( $image_data );
					$image_name = ($base_time ++) . '.jpg';
					$file = UPLOAD_BASE_PATH . $user_id . DIRECTORY_SEPARATOR . $image_name;
					log_message ( 'debug', "Upload.image: Save the uploaded jpg to $image_name" );
					file_put_contents ( $file, $image_data );
					array_push ( $image_names, $image_name );
				}
			}
		}
		
		return $image_names;
	}
	private function save_uploaded_image_bak($user_id) {
		$upload_path = UPLOAD_BASE_PATH . $user_id;
		if (! file_exists ( $upload_path )) {
			mkdir ( $upload_path, 0777, true );
		}
		
		$config ['upload_path'] = $upload_path;
		$config ['allowed_types'] = 'gif|jpg|png';
		$config ['max_size'] = '5120';
		$config ['overwrite'] = TRUE;
		$this->load->library ( 'upload', $config );
		
		$image_names = array ();
		$base_time = time ();
		for($i = 0; $i < 5; $i ++) {
			$image_name = ($base_time + $i) . '.jpg';
			$config ['file_name'] = $image_name;
			$this->upload->initialize ( $config );
			if (! $this->upload->do_upload ( 'image_file_' . $i )) {
				break;
			}
			log_message ( 'debug', 'save image successfully. image_name = ' . $image_name );
			$image_names [$i] = $image_name;
		}
		
		return $image_names;
	}
	private function save_item($user_id, $image_names) {
		// Build item data
		$this->load->helper ( 'uuid' );
		$item_id = gen_uuid ();
		$date_now = date ( 'Y-m-d H:i:s' );
		$title = $this->input->post ( 'title' );
		$description = $this->input->post ( 'description' ) . "\n\n";
		$description .= 'Email: ' . $this->input->post ( 'email' ) . "\n";
		if ($this->input->post ( 'wechatId' ))
			$description .= 'WeChat ID: ' . $this->input->post ( 'wechatId' ) . "\n";
		if ($this->input->post ( 'zipcode' ))
			$description .= 'ZIP Code: ' . $this->input->post ( 'zipcode' );
		
		$input_data ['itemId'] = $item_id;
		$input_data ['userId'] = $user_id;
		$input_data ['inputSource'] = 'WEB';
		$input_data ['title'] = $title;
		$input_data = array_merge ( $input_data, $this->query_category_by_title ( $title ) );
		$input_data ['expectedPrice'] = $this->input->post ( 'price' );
		$input_data ['condition'] = $this->input->post ( 'condition' );
		$input_data ['availability'] = 'XX';
		$input_data ['desc'] = $description;
		$input_data ['recCreateTime'] = $date_now;
		$input_data ['recUpdateTime'] = $date_now;
		$input_data ['synchWp'] = 'N';
		
		$this->load->helper ( 'location' );
		$loc = get_loc_by_zipcode ( $this->input->post ( 'zipcode' ) );
		if ($loc) {
			$input_data ['latitude'] = $loc ['latitude'];
			$input_data ['longitude'] = $loc ['longitude'];
			$input_data ['region'] = build_region_string_by_loc ( $loc );
		}
		
		$this->db->trans_start ();
		
		// insert the itme into item table
		$this->item_model->insert_item ( $input_data );
		$item = $this->item_model->get_item ( $item_id );
		$global_item_id = $item ['Global_Item_ID'];
		
		// insert image names into item_image table
		foreach ( $image_names as $image_name ) {
			$this->item_model->insert_image ( $global_item_id, $image_name );
		}
		
		$this->db->trans_complete ();
		
		if ($this->db->trans_status () === FALSE) {
			return FALSE;
		}
		
		log_message ( 'debug', 'save the item successfully. global_item_id = ' . $global_item_id );
		
		return $item;
	}
	private function sync_item_to_wordpress($global_item_id, $user_id) {
		log_message ( 'debug', 'Start to synchronize the item to WordPress DB.' );
		$this->load->helper ( 'sync' );
		$wp_item = create_wp_item ( $global_item_id, $this->item_model, $this->meta_model );
		if (! $wp_item) {
			return FALSE;
		}
		$image_row_array = $this->item_model->get_images ( $global_item_id );
		
		$wp_db = $this->load->database ( 'wp', TRUE );
		if (! $wp_db->initialize ()) {
			log_message ( 'error', 'Item.synch_item: Failed to connect the database.' );
			return FALSE;
		}
		$this->wordpress_model->db = $wp_db;
		return sync_wp_item ( $global_item_id, $user_id, $wp_item, $image_row_array, $this->wordpress_model );
	}
	private function send_item_success_email($item, $email, $activity_id) {
		$this->load->helper ( 'uuid' );
		$this->load->helper ( 'myemail' );
		
		$email_subject = 'POST/EDIT: "' . $item ['title'] . '"';
		$email_body = $this->load->view ( 'activity/item_success_message_body', array (
				'b64_item_id' => encode_uuid_base64 ( $item ['itemId'] ),
				'activity_id' => $activity_id 
		), TRUE );
		
		$fields = array (
				'from' => 'Weee! Automated message do not reply <robot@letustag.com>',
				'to' => $email,
				'subject' => $email_subject,
				'html' => $email_body 
		);
		send_email ( null, $email, $email_subject, $email_body );
	}
	public function activate_item($b64_item_id, $activity_id = 1) {
		$item = $this->query_item_by_b64uuid ( $b64_item_id );
		$activity = $this->activity_model->get_activity ( $activity_id );
		if (! $item || ! $activity) {
			show_error ( 'Invalid URL' );
			return;
		}
		
		// mark the item as 'For Sale'
		$this->item_model->update_item ( array (
				'itemId' => $item ['itemId'],
				'availability' => 'AB',
				'recUpdateTime' => date ( 'Y-m-d H:i:s' ) 
		) );
		
		// add the item into the activity
		$global_item_id = $item ['Global_Item_ID'];
		$this->activity_model->insert_activity_item_relation ( $activity_id, $global_item_id );
		if ($activity ['Global_Catalogue_ID']) {
			$this->activity_model->insert_item_into_catalog ( $activity ['Global_Catalogue_ID'], $global_item_id );
		}
		
		// synchronize WordPress DB
		$result = $this->sync_item_to_wordpress ( $global_item_id, $item ['userId'] );
		if (! $result) {
			$data ['error'] = 'Failed to update the WordPress database.';
			return $this->load_edit_item_view ( $data );
		}
		$this->wordpress_model->insert_activity_item_relation ( $activity_id, $global_item_id );
		
		$data ['title'] = 'Success - Publish Your Item';
		$data ['activity_url'] = $activity ['Post_URL'];
		$data ['product_url'] = $this->get_product_url ( $activity ['Post_URL'], $global_item_id );
		
		$this->load->view ( 'templates/web_header', $data );
		$this->load->view ( 'activity/activate_item_success', $data );
		$this->load->view ( 'templates/web_footer', $data );
	}
	public function edit_item($b64_item_id, $activity_id = 1) {
		$item = $this->query_item_by_b64uuid ( $b64_item_id );
		$activity = $this->activity_model->get_activity ( $activity_id );
		if (! $item || ! $activity) {
			show_error ( 'Invalid URL' );
			return;
		}
		
		$global_item_id = $item ['Global_Item_ID'];
		$user_id = $item ['userId'];
		$image_rows = $this->item_model->get_images ( $global_item_id );
		$user = $this->user_model->get_user ( $user_id );
		
		$data ['title'] = 'Edit Item - ' . $activity ['Activity_Name'];
		$data ['b64_item_id'] = $b64_item_id;
		$data ['activity'] = $activity;
		$data ['item'] = $item;
		$data ['user'] = $user;
		$data ['image_url_base'] = '/images/weee_app/' . $user_id . '/';
		$data ['images'] = $image_rows;
		$data ['error'] = '';
		
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		$this->form_validation->set_rules ( 'title', 'Title', 'required' );
		$this->form_validation->set_rules ( 'price', 'Price', 'required|numeric' );
		$this->form_validation->set_rules ( 'condition', 'Condition', 'required' );
		$this->form_validation->set_rules ( 'description', 'Description', 'required' );
		
		if (! $this->form_validation->run ()) {
			return $this->load_edit_item_view ( $data );
		}
		
		$image_names = $this->save_uploaded_image ( $user ['userId'] );
		$old_image_names = $this->input->post ( 'image_file_names' );
		if (! $old_image_names && count ( $image_names ) == 0) {
			$data ['error'] = 'Please choose the picture.';
			log_message ( 'debug', print_r ( $data, true ) );
			return $this->load_edit_item_view ( $data );
		}
		// insert new images;
		if (count ( $image_names ) > 0) {
			foreach ( $image_names as $image_name ) {
				$this->item_model->insert_image ( $global_item_id, $image_name );
			}
		}
		// delete removeded old images
		foreach ( $image_rows as $image_row ) {
			if (! in_array ( $image_row ['imageName'], $old_image_names ))
				$this->item_model->delete_image ( $global_item_id, $image_row ['imageName'] );
		}
		
		// save the item into the DB
		$title = $this->input->post ( 'title' );
		$category = $this->query_category_by_title ( $title );
		$success = $this->item_model->update_item ( array (
				'itemId' => $item ['itemId'],
				'title' => $title,
				'category' => $category ['category'],
				'catNum' => $category ['catNum'],
				'expectedPrice' => $this->input->post ( 'price' ),
				'condition' => $this->input->post ( 'condition' ),
				'desc' => $this->input->post ( 'description' ),
				'recUpdateTime' => date ( 'Y-m-d H:i:s' ),
				'synchWp' => 'N' 
		) );
		if (! $success) {
			log_message ( 'error', 'Activity.edit_item: Failed to update the database.' );
			$data ['error'] = 'Failed to update the database.';
			return $this->load_edit_item_view ( $data );
		}
		
		// synchronize to wp database
		$result = $this->sync_item_to_wordpress ( $global_item_id, $user_id );
		if (! $result) {
			$data ['error'] = 'Failed to update the WordPress database.';
			return $this->load_edit_item_view ( $data );
		}
		
		// call python script to resize and upload image files
		resize_upload_images ( $global_item_id, $this->item_model );
		
		// output
		$data ['title'] = 'Success - Edit Your Item';
		$data ['activity_url'] = $activity ['Post_URL'];
		$data ['product_url'] = $this->get_product_url ( $activity ['Post_URL'], $global_item_id );
		
		$this->load->view ( 'templates/web_header', $data );
		$this->load->view ( 'activity/edit_item_success', $data );
		$this->load->view ( 'templates/web_footer', $data );
		return;
	}
	private function load_edit_item_view($data) {
		$data ['meta_condition'] = $this->meta_model->get_meta_code_array ( META_TYPE_CONDITION );
		
		$this->load->view ( 'templates/web_header', $data );
		$this->load->view ( 'activity/edit_item', $data );
		$this->load->view ( 'templates/web_footer', $data );
	}
	public function sold_item($b64_item_id, $activity_id = 1) {
		$item = $this->query_item_by_b64uuid ( $b64_item_id );
		$activity = $this->activity_model->get_activity ( $activity_id );
		if (! $item || ! $activity) {
			show_error ( 'Invalid URL' );
			return;
		}
		
		$global_item_id = $item ['Global_Item_ID'];
		
		$result = $this->item_model->update_item ( array (
				'itemId' => $item ['itemId'],
				'availability' => 'SD',
				'recUpdateTime' => date ( 'Y-m-d H:i:s' ) 
		) );
		if ($result) {
			$this->sync_item_to_wordpress ( $global_item_id, $item ['userId'] );
			if ($result) {
				$data ['title'] = 'Success - Mark Your Item as Sold';
				$data ['activity_url'] = $activity ['Post_URL'];
				$data ['product_url'] = $this->get_product_url ( $activity ['Post_URL'], $global_item_id );
				
				$this->load->view ( 'templates/web_header', $data );
				$this->load->view ( 'activity/sold_item_success', $data );
				$this->load->view ( 'templates/web_footer', $data );
				return;
			}
		}
		echo 'Failed to mark the item as sold.';
	}
	private function get_product_url($activity_url, $global_item_id) {
		if (strpos ( $activity_url, '?' ) !== false)
			return $activity_url . '&SingleProduct=' . $global_item_id;
		else
			return $activity_url . '?SingleProduct=' . $global_item_id;
	}
	private function query_item_by_b64uuid($b64_item_id) {
		$this->load->helper ( 'uuid' );
		$item_id = decode_uuid_base64 ( $b64_item_id );
		
		$item = $this->item_model->get_item ( $item_id );
		if (! $item) {
			$item = $this->item_model->get_item ( strtoupper ( $item_id ) );
		}
		return $item;
	}
	private function query_category_by_title($title) {
		$this->load->helper ( 'script' );
		$categories = call_script ( 'query_categories_by_title.py', array (
				$title 
		) );
		
		if (is_array ( $categories ) && count ( $categories ) > 0) {
			$best_category = $categories [0];
			foreach ( $categories as $category ) {
				// For algorithm traning purpose, the first one is't best one now.
				// Current we think the category commended by ebay is better.
				// algoType 0 is our machine learning offline alog
				// algoType 1 ebay api
				// algoType 2 is a result returned by both algos.
				
				if ($category ['algoType'] == 1 || $category ['algoType'] == 2) {
					$best_category = $category;
					break;
				}
			}
			return array (
					'category' => $best_category ['catCode'],
					'catNum' => $best_category ['catNum'] 
			);
		}
		return array (
				'category' => 'ELS',
				'catNum' => '000' 
		);
	}
}

?>
