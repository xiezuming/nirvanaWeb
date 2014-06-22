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
		if (empty ( $userName ) || empty ( $password )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: UserName or password is empty.';
		} else {
			$user = $this->user_model->query_user ( $userName );
			if ($user) {
				$data ['result'] = FAILURE;
				$data ['message'] = 'The user exists.';
			} else {
				$userId = $this->user_model->create_user ( $userName, $password );
				$data ['result'] = SUCCESS;
				$data ['data'] = array (
						'userId' => $userId 
				);
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function sign_in() {
		$userName = $this->input->post ( 'userName' );
		$password = $this->input->post ( 'password' );
		$user = NULL;
		if (empty ( $userName ) || empty ( $password )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: UserName or password is empty.';
		} else {
			$user = $this->user_model->query_user ( $userName );
			if ($user) {
				if ($user ['password'] == md5 ( $password )) {
					$data ['result'] = SUCCESS;
					$data ['data'] = array (
							'userId' => $user ['userId'] 
					);
				} else {
					$data ['result'] = FAILURE;
					$data ['message'] = 'That password is incorrect. Be sure you\'re using the password for your WeTag account.';
				}
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = 'That WeTag account doesn\'t exist. Enter a different email address or get a new account';
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
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
