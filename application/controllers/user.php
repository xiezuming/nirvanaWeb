<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;

/**
 *
 * @property User_model $user_model
 */
class User extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'user_model' );
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->view ( 'user/user_form' );
	}
	public function create_user() {
		$userName = $this->input->post ( 'userName' );
		$password = $this->input->post ( 'password' );
		echo $this->user_model->create_user ( $userName, $password );
	}
	public function login() {
		$userName = $this->input->post ( 'userName' );
		$password = $this->input->post ( 'password' );
		$user = NULL;
		if ($userName && $password) {
			$user = $this->user_model->login ( $userName, $password );
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
			$user = $this->user_model->logout ( $userId );
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
}

?>
