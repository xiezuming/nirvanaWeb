<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const UPLOAD_BASE_PATH = '/var/uploads/wetag_app/';
const DEFAULT_SHARE_USER_ID = 'fd3142d3-167b-48c5-8208-2762e2db2fb2';
const DEFAULT_CATALOGUE_GLOBAL_ID = '1051';

/**
 *
 * @property Item_model $item_model
 * @property User_model $user_model
 * @property Meta_model $meta_model
 */
class Admin_item extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'item_model' );
		$this->load->model ( 'user_model' );
		$this->load->model ( 'meta_model' );
	}
	/* ---------------- page entry ---------------- */
	public function index() {
		$items = $this->item_model->query_items ( NULL, 5 );
		$item_list = array ();
		foreach ( $items as $item ) {
			$user = $this->user_model->get_user ( $item ['userId'] );
			$item ['user'] = '[' . $user ['userType'] . ']' . $user ['email'];
			array_push ( $item_list, $item );
		}
		
		$data ['title'] = 'Item List';
		$data ['items'] = $item_list;
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'admin_item/list', $data );
		$this->load->view ( 'templates/footer' );
	}
	public function view($global_item_id) {
		$item = $this->item_model->get_item_by_global_id ( $global_item_id );
		$images = $this->item_model->get_images ( $global_item_id );
		$users = $this->user_model->query_all_users ();
		$user_select_list = array ();
		foreach ( $users as $user ) {
			$user_select_list [$user ['userId']] = $user ['userType'] . '|' . $user ['email'];
		}
		asort ( $user_select_list );
		$user = $this->user_model->get_user ( $item ['userId'] );
		$user ['password'] = '********';
		
		$data ['title'] = 'Item Details';
		$data ['item'] = $item;
		$data ['images'] = $images;
		$data ['user'] = $user;
		$data ['user_select_list'] = $user_select_list;
		$this->load->helper ( 'form' );
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'admin_item/view', $data );
		$this->load->view ( 'templates/footer' );
	}
	public function copy($soruce_global_item_id, $dest_user_id) {
		$source_item = $this->item_model->get_item_by_global_id ( $soruce_global_item_id );
		$dest_user = $this->user_model->get_user ( $dest_user_id );
		if (! $source_item || ! $dest_user || $source_item ['userId'] == $dest_user_id) {
			show_error ( 'Invalid argument' );
			return;
		}
		
		// Insert into item table
		$dest_item = $source_item;
		$this->load->helper ( 'uuid' );
		$dest_item_id = gen_uuid ();
		$date_now = date ( 'Y-m-d H:i:s' );
		unset ( $dest_item ['Global_Item_ID'] );
		$dest_item ['itemId'] = $dest_item_id;
		$dest_item ['userId'] = $dest_user_id;
		$dest_item ['recCreateTime'] = $date_now;
		$dest_item ['recUpdateTime'] = $date_now;
		$dest_item ['synchWp'] = 'N';
		$dest_item ['sourceItemId'] = $soruce_global_item_id;
		$result = $this->item_model->insert_item ( $dest_item );
		if (! $result) {
			echo 'Failed to insert item table.';
			return;
		}
		$dest_item = $this->item_model->get_item ( $dest_item_id );
		$dest_global_item_id = $dest_item ['Global_Item_ID'];
		
		$source_image_folder = UPLOAD_BASE_PATH . DIRECTORY_SEPARATOR . $source_item ['userId'];
		$dest_image_folder = UPLOAD_BASE_PATH . DIRECTORY_SEPARATOR . $dest_item ['userId'];
		if (! file_exists ( $dest_image_folder )) {
			mkdir ( $dest_image_folder, 0777, true );
		}
		$images = $this->item_model->get_images ( $soruce_global_item_id );
		foreach ( $images as $image ) {
			$source_image_file = $source_image_folder . DIRECTORY_SEPARATOR . $image ['imageName'];
			$dest_image_file = $dest_image_folder . DIRECTORY_SEPARATOR . $image ['imageName'];
			if (! copy ( $source_image_file, $dest_image_file )) {
				echo "failed to copy $source_image_file";
				return;
			}
			$this->item_model->insert_image ( $dest_global_item_id, $image ['imageName'] );
		}
		
		$this->load->helper ( 'url' );
		redirect ( site_url ( '/item/synch_item/' . $dest_global_item_id ), 'refresh' );
	}
}

?>
