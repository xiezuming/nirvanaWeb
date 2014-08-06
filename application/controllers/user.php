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
	public function sign_up() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$this->form_validation->set_rules ( 'userName', 'User Name', 'required|valid_email|max_length[45]|is_unique[user.userName]' );
		$this->form_validation->set_rules ( 'firstName', 'First Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'lastName', 'Last Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'password', 'Password', 'required|matches[password_confirm]' );
		$this->form_validation->set_rules ( 'password_confirm', 'Password Confirmation', 'required' );
		$this->form_validation->set_rules ( 'phoneNumber', 'Phone Number', 'max_length[45]' );
		$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', 'max_length[45]' );
		
		if ($this->input->post () && $this->form_validation->run ()) {
			if ($this->user_model->create_user ( $this->input->post () )) {
				$this->load->view ( 'user/jump_sign_up_success' );
				return;
			} else {
				echo "DB ERROR.";
				return;
			}
		}
		$data = $this->input->post ();
		$data ['title'] = 'Sign Up';
		$this->load->view ( 'templates/header_app', $data );
		$this->load->view ( 'user/sign_up', $data );
		$this->load->view ( 'templates/footer_app' );
	}
	public function sign_up_success() {
		echo "SUCCESS";
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
