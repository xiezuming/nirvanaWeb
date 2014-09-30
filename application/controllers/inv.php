<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const UPLOAD_BASE_PATH = '/var/uploads/';

/**
 * 
 * @property Item_model $item_model
 * @property User_model $user_model
 * @property Inv_recommendation_model $inv_recommendation_model
 */
class Inv extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'item_model' );
		$this->load->model ( 'user_model' );
		$this->load->model ( 'inv_recommendation_model' );
	}

	public function user_page() {
		$this->load->helper ( 'form' );
		$this->load->view ( 'user/user_form' );
	}
	public function create_user() {
		$userName = $this->input->post ( 'userName' );
		$password = $this->input->post ( 'password' );
		echo $this->inv_user_model->create_user ( $userName, $password );
	}
	public function login() {
		$userName = $this->input->post ( 'userName' );
		$password = $this->input->post ( 'password' );
		$user = NULL;
		if ($userName && $password) {
			$user = $this->inv_user_model->login ( $userName, $password );
		}
		if ($user) {
			$data ['result'] = SUCCESS;
			$data ['data'] = $user;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Username and password do not match.';
		}
		echo json_encode ( $data );
	}
	public function logout() {
		$userId = $this->input->post ( 'userId' );
		if ($userId) {
			$user = $this->inv_user_model->logout ( $userId );
		}
	}
	private function check_token() {
		// TODO add token check
		return NULL;
		$userId = $this->input->post ( 'userId' );
		$token = $this->input->post ( 'token' );
		$check = $this->inv_user_model->check_user ( $userId, $token );
		if ($check) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Token Error.';
			return $data;
		}
	}
	
	public function add_item() {
		$check = $this->check_token ();
		if ($check) {
			echo json_encode ( $check );
			return;
		}
		$input_data = $this->get_input_data ();
		$inv_item = $this->inv_item_model->get_inv_item ( $input_data ['userId'], $input_data ['itemId'] );
		if ($inv_item) {
			$this->inv_item_model->delete_inv_itme ( $inv_item );
			
			$path = UPLOAD_BASE_PATH . $inv_item ['userId'] . '/';
			if ($inv_item ['photoname1'])
				$this->delete_file ( $path . $inv_item ['photoname1'] );
			if ($inv_item ['photoname2'])
				$this->delete_file ( $path . $inv_item ['photoname2'] );
			if ($inv_item ['photoname3'])
				$this->delete_file ( $path . $inv_item ['photoname3'] );
		}
		$data ['result'] = $this->inv_item_model->add_inv_item ( $input_data ) ? SUCCESS : FAILURE;
		
		echo json_encode ( $data );
	}
	private function delete_file($file_path) {
		if (file_exists ( $file_path )) {
			unlink ( $file_path );
		}
	}
	public function item_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'inv/add_form', $data );
	}
	function upload() {
		$check = $this->check_token ();
		if ($check) {
			echo json_encode ( $check );
			return;
		}
		
		$userId = $this->input->post ( 'userId' );
		$upload_path = UPLOAD_BASE_PATH . $userId;
		if (! file_exists ( $upload_path )) {
			mkdir ( $upload_path );
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
		
		echo json_encode ( $data );
	}
	public function upload_page() {
		$this->load->helper ( 'form' );
		
		$this->load->view ( 'inv/upload_form', array (
				'error' => ' ' 
		) );
	}
	public function query_recommendation_info() {
		$check = $this->check_token ();
		if ($check) {
			echo json_encode ( $check );
			return;
		}
		
		$input_data = $this->input->post ();
		if (isset ( $input_data['barcode'] )) {
			$inv_search_result = $this->inv_recommendation_model->query_recommended_info ( $input_data );
			if ($inv_search_result) {
				$data ['result'] = SUCCESS;
				$data ['data'] = $inv_search_result;
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = 'There is no matched item in the server.';
			}
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error.';
		}
		echo json_encode ( $data );
	}
	public function query_item_price() {
		$check = $this->check_token ();
		if ($check) {
			echo json_encode ( $check );
			return;
		}
		
		$barcode = $this->input->post ( 'barcode' );
		$title = $this->input->post ( 'title' );
		if (isset ( $barcode ) || isset ( $title )) {
			$inv_search_result = $this->inv_recommendation_model->query_inv_price ( $barcode, $title );
			if ($inv_search_result) {
				$data ['result'] = SUCCESS;
				$data ['data'] = $inv_search_result;
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = 'There is no matched item in the server.';
			}
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error.';
		}
		echo json_encode ( $data );
	}
	private function get_field_names() {
		$field_names = array (
				"userId" => "userId",
				"itemId" => "itemId",
				"title" => "title",
				"barcode" => "barcode",
				"market" => "market",
				"status" => "status",
				"category" => "category",
				"condition" => "condition",
				"price" => "price",
				"quantity" => "quantity",
				"size" => "size",
				"weight" => "weight",
				"latitude" => "latitude",
				"longitude" => "longitude",
				"desc" => "desc",
				"photoname1" => "photoname1",
				"photoname2" => "photoname2",
				"photoname3" => "photoname3",
				"createDate" => "createDate",
				"updateDate" => "updateDate" 
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
				if ($this->endsWith ( $field_name, 'Date' )) {
					$field_value = date ( 'Y-m-d H:i:s', $field_value );
				}
				$input_data [$field_name] = $field_value;
			}
		}
		return $input_data;
	}
	private function endsWith($haystack, $needle) {
		return $needle === "" || substr ( $haystack, - strlen ( $needle ) ) === $needle;
	}
}

?>
