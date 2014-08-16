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
		
		$this->form_validation->set_rules ( 'userName', 'Email Address', 'required|valid_email|max_length[45]|is_unique[user.userName]' );
		$this->form_validation->set_rules ( 'firstName', 'First Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'lastName', 'Last Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'password', 'Password', 'required|matches[password_confirm]' );
		$this->form_validation->set_rules ( 'password_confirm', 'Password Confirmation', 'required' );
		$this->form_validation->set_rules ( 'phoneNumber', 'Phone Number', 'max_length[45]' );
		$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', 'max_length[45]' );
		$this->form_validation->set_rules ( 'zipcode', 'ZIP Code', 'max_length[10]' );
		
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
					$user ['password'] = '';
					$data ['data'] = $user;
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
	public function reset_password_mail() {
		$this->load->helper ( 'url' );
		
		if (! isset ( $_POST ['email_address'] )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'The email is empty';
		} else {
			$email_address = $this->input->post ( 'email_address', true );
			log_message ( 'debug', 'User.reset_password_mail: $email_address = ' . $email_address );
			
			$user = $this->user_model->query_user ( $email_address );
			
			if ($user) {
				$user_id = $user ['userId'];
				$reset_key = $this->user_model->create_reset_key ( $user_id );
				if ($reset_key) {
					// load email library
					$this->load->library ( 'email' );
					// construct email
					$this->email->from ( 'noreply@wetagapp.com', "WeTag" );
					$this->email->to ( $email_address );
					$this->email->subject ( "[WeTag] How to reset your password" );
					$link = site_url ( 'user/reset_password/' . $user_id . '/' . $reset_key );
					$this->email->message ( $this->load->view ( 'user/reset_password_mail', array (
							'link' => $link 
					), TRUE ) );
					if ($this->email->send ()) {
						$data ['result'] = SUCCESS;
						$data ['message'] = 'Instructions on how to reset your password have been sent to ' . $email_address . '.';
					} else {
						log_message ( 'error', 'Can not send the email: ' . $this->email->print_debugger () );
						$data ['result'] = FAILURE;
						$data ['message'] = 'Internal Error: Can not send the email.';
					}
				} else {
					$data ['result'] = FAILURE;
					$data ['message'] = 'Internal Error';
				}
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = 'The email is invalid';
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function reset_password($user_id = '', $reset_key = '') {
		if (empty ( $user_id ))
			$user_id = $this->input->post ( 'user_id' );
		if (empty ( $reset_key ))
			$reset_key = $this->input->post ( 'reset_key' );
		
		if (empty ( $user_id ) || empty ( $reset_key )) {
			show_error ( 'Error URL.' );
		}
		
		$reset_row = $this->user_model->get_reset_row ( $reset_key );
		if (! $reset_row || $reset_row ['userId'] != $user_id) {
			show_error ( 'Error URL.' );
		}
		
		$key_used = $reset_row ['key_used'];
		if ($key_used != 'N') {
			show_error ( 'Used key. Send reset request again.' );
		}
		
		$request_time = $reset_row ['request_time'];
		if (time () - strtotime ( $request_time ) > 3600) { // 1 Hour
			show_error ( 'Invalid key. Send reset request again.' );
		}
		
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$this->form_validation->set_rules ( 'password', 'Password', 'required|matches[password_confirm]' );
		$this->form_validation->set_rules ( 'password_confirm', 'Password Confirmation', 'required' );
		
		if ($this->input->post () && $this->form_validation->run ()) {
			if ($this->user_model->reset_password ( $user_id, $this->input->post ( 'password' ) )) {
				$this->user_model->clear_reset_key ( $reset_key );
				$data ['title'] = 'Reset Password';
				$this->load->view ( 'templates/header', $data );
				$this->load->view ( 'user/reset_password_success', $data );
				$this->load->view ( 'templates/footer' );
				return;
			} else {
				show_error ( 'DB Error.' );
			}
		}
		
		$data ['title'] = 'Reset Password';
		$data ['user_id'] = $user_id;
		$data ['reset_key'] = $reset_key;
		
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'user/reset_password', $data );
		$this->load->view ( 'templates/footer' );
	}
	public function update_wish_list() {
		$user_id = $this->input->post ( 'userId' );
		$wish_list = $this->input->post ( 'wishList' );
		if (empty ( $user_id )) {
			$data ['result'] = FAILURE;
			$data ['userId'] = 'Internal Error: userId is empty.';
		} else {
			if ($this->user_model->update_wish_list ( $user_id, $wish_list )) {
				$data ['result'] = SUCCESS;
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = 'Failed to update DB.';
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
}

?>
