<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

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
		$this->form_validation->set_rules ( 'firstName', 'First Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'lastName', 'Last Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'email', 'Email Address', 'required|valid_email|max_length[45]|callback_email_check' );
		$this->form_validation->set_rules ( 'password', 'Password', 'required|matches[password_confirm]' );
		$this->form_validation->set_rules ( 'password_confirm', 'Password Confirmation', 'required' );
		$this->form_validation->set_rules ( 'zipcode', 'ZIP Code', 'required|max_length[10]' );
		$this->form_validation->set_rules ( 'phoneNumber', 'Phone Number', 'max_length[45]' );
		$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', 'max_length[45]' );
		
		if ($this->form_validation->run ()) {
			$input_data = $this->input->post ();
			$input_data ['userType'] = USER_TYPE_WETAG;
			$input_data ['alias'] = $input_data ['firstName'];
			$user_id = $this->user_model->create_user ( $input_data );
			if ($user_id) {
				$this->load->view ( 'user/jump_sign_up_success' );
				return;
			} else {
				echo "DB ERROR.";
				return;
			}
		}
		
		$data ['title'] = 'Sign Up';
		$this->load->view ( 'templates/header_app', $data );
		$this->load->view ( 'user/sign_up', $data );
		$this->load->view ( 'templates/footer_app' );
	}
	public function sign_up_success() {
		echo "SUCCESS";
	}
	public function api_get_user_info($user_id) {
		$user = $this->user_model->get_user ( $user_id );
		if ($user) {
			$data ['result'] = SUCCESS;
			$data ['data'] = $user;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'No User.';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function api_edit_profile() {
		$this->load->helper ( 'form' );
		
		$user_id = $this->input->post ( 'userId' );
		// init load
		if (! $user_id) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error';
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		$user = $this->user_model->get_user ( $user_id );
		if (! $user) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Can not find the user.';
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		
		$this->load->library ( 'form_validation' );
		$this->form_validation->set_rules ( 'firstName', 'First Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'lastName', 'Last Name', 'required|max_length[45]' );
		$this->form_validation->set_rules ( 'alias', 'Alias', 'required|max_length[45]' );
		$email = $this->input->post ( 'email' );
		$check_email = ($email === $user ['email']) ? '' : '|callback_email_check';
		$this->form_validation->set_rules ( 'email', 'Email Address', 'required|valid_email|max_length[45]' . $check_email );
		$this->form_validation->set_rules ( 'password', 'Password', '' );
		$this->form_validation->set_rules ( 'zipcode', 'ZIP Code', 'required|max_length[10]' );
		$this->form_validation->set_rules ( 'phoneNumber', 'Phone Number', 'max_length[45]' );
		$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', 'max_length[45]' );
		
		if (! $this->form_validation->run ()) {
			$this->form_validation->set_error_delimiters ( '', '' );
			$data ['result'] = FAILURE;
			$data ['message'] = validation_errors ();
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		$input = $this->input->post ();
		$update_data = array (
				'firstName' => $input ['firstName'],
				'lastName' => $input ['lastName'],
				'alias' => $input ['alias'],
				'email' => $input ['email'],
				'phoneNumber' => $input ['phoneNumber'],
				'wechatId' => $input ['wechatId'],
				'zipcode' => $input ['zipcode'] 
		);
		if (! empty ( $input ['password'] )) {
			$update_data ['password'] = md5 ( $input ['password'] );
		}
		$success = $this->user_model->update_user ( $user_id, $update_data );
		if ($success) {
			$data ['data'] = $this->user_model->get_user ( $user_id );
			$data ['result'] = SUCCESS;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Failed to update the database.';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function sign_in() {
		$email = $this->input->post ( 'email' );
		$password = $this->input->post ( 'password' );
		$user = NULL;
		if (empty ( $email ) || empty ( $password )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: email or password is empty.';
		} else {
			$user = $this->user_model->query_user ( array (
					'email' => $email 
			) );
			if ($user) {
				if ($user ['password'] == md5 ( $password )) {
					$this->_update_user_app_login_time ( $user ['userId'] );
					$data ['result'] = SUCCESS;
					$data ['data'] = $user;
				} else {
					$data ['result'] = FAILURE;
					$data ['message'] = lang ( 'error_password_mismatch' );
				}
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = lang ( 'error_account_notexist' );
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function sign_in_fb() {
		$input_data = $this->input->post ();
		$fbUserId = $input_data ['fbUserId'];
		if (empty ( $fbUserId )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Facebook user id is empty.';
		} else {
			$user = $this->user_model->query_user ( array (
					'fbUserId' => $fbUserId 
			) );
			if ($user) {
				$user_id = $user ['userId'];
			} else {
				$input_data ['userType'] = USER_TYPE_FACEBOOK;
				$input_data ['alias'] = $input_data ['firstName'];
				$user_id = $this->user_model->create_user ( $input_data );
				if (! $user_id) {
					$data ['result'] = FAILURE;
					$data ['message'] = 'Internal Error: Falied to crate the user.';
				}
			}
			if ($user_id) {
				$this->_update_user_app_login_time ( $user_id );
				$data ['result'] = SUCCESS;
				$data ['data'] = $this->user_model->get_user ( $user_id );
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function sign_in_wx() {
		$input_data = $this->input->post ();
		$wxUnionId = $input_data ['wxUnionId'];
		if (empty ( $wxUnionId )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Weixin user union id is empty.';
		} else {
			$user = $this->user_model->query_user ( array (
					'wxUnionId' => $wxUnionId 
			) );
			if ($user) {
				$user_id = $user ['userId'];
			} else {
				$input_data ['userType'] = USER_TYPE_WEIXIN;
				$input_data ['firstName'] = $input_data ['alias'];
				$input_data ['lastName'] = 'Weee!';
				$user_id = $this->user_model->create_user ( $input_data );
				if (! $user_id) {
					$data ['result'] = FAILURE;
					$data ['message'] = 'Internal Error: Falied to crate the user.';
				}
			}
			if ($user_id) {
				$this->_update_user_app_login_time ( $user_id );
				$data ['result'] = SUCCESS;
				$data ['data'] = $this->user_model->get_user ( $user_id );
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function reset_password_mail() {
		$this->load->helper ( 'url' );
		
		if (! isset ( $_POST ['email_address'] )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: The email is empty';
		} else {
			$email_address = $this->input->post ( 'email_address', true );
			log_message ( 'debug', 'User.reset_password_mail: $email_address = ' . $email_address );
			
			$user = $this->user_model->query_user ( $where = array (
					'email' => $email_address,
					'userType' => USER_TYPE_WETAG 
			) );
			
			if ($user) {
				$user_id = $user ['userId'];
				$reset_key = $this->user_model->create_reset_key ( $user_id );
				if ($reset_key) {
					$subject = '[Weee!] How to reset your password';
					$link = site_url ( 'user/reset_password/' . $user_id . '/' . $reset_key );
					$body_html = $this->load->view ( 'user/reset_password_mail', array (
							'link' => $link 
					), TRUE );
					$this->load->helper ( 'myemail' );
					$result = send_email ( null, $email_address, $subject, $body_html );
					if ($result) {
						$data ['result'] = SUCCESS;
						$data ['message'] = sprintf ( $this->lang->line ( 'info_reset_password_response' ), $email_address );
					} else {
						$data ['result'] = FAILURE;
						$data ['message'] = 'Internal Error: Can not send the email.';
					}
				} else {
					$data ['result'] = FAILURE;
					$data ['message'] = 'Internal Error';
				}
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = lang ( 'error_no_email_account' );
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
			show_error ( lang ( 'error_reset_link_used' ) );
		}
		
		$request_time = $reset_row ['request_time'];
		if (time () - strtotime ( $request_time ) > 3600) { // 1 Hour
			show_error ( lang ( 'error_reset_link_timeout' ) );
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
	public function api_send_verify_mail($user_id) {
		$this->load->helper ( 'url' );
		
		$user = $this->user_model->get_user ( $user_id );
		if (! $user || empty ( $user ['email'] )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: The email address is empty.';
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		
		$email_address = $user ['email'];
		$reset_key = $this->user_model->create_reset_key ( $user_id, $email_address );
		if ($reset_key) {
			$this->load->helper ( 'uuid' );
			$subject = '[Weee!] Verify your email address';
			$link = site_url ( 'user/verify_email/' . encode_uuid_base64 ( $user_id ) . '/' . encode_uuid_base64 ( $reset_key ) );
			$body_html = $this->load->view ( 'user/verification_mail', array (
					'link' => $link 
			), TRUE );
			$this->load->helper ( 'myemail' );
			$result = send_email ( null, $email_address, $subject, $body_html );
			if ($result) {
				$data ['result'] = SUCCESS;
				$data ['message'] = sprintf ( $this->lang->line ( 'info_verify_email_response' ), $email_address );
			} else {
				$data ['result'] = FAILURE;
				$data ['message'] = 'Internal Error: Can not send the email.';
			}
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function verify_email($user_id = '', $reset_key = '') {
		if (empty ( $user_id ) || empty ( $reset_key )) {
			show_error ( 'Error URL.' );
		}
		$this->load->helper ( 'uuid' );
		
		$user_id = decode_uuid_base64 ( $user_id );
		$reset_key = decode_uuid_base64 ( $reset_key );
		
		$reset_row = $this->user_model->get_reset_row ( $reset_key );
		if (! $reset_row || $reset_row ['userId'] != $user_id) {
			show_error ( 'Error URL.' );
		}
		
		$key_used = $reset_row ['key_used'];
		if ($key_used != 'N') {
			show_error ( lang ( 'error_verify_link_used' ) );
		}
		
		$request_time = $reset_row ['request_time'];
		if (time () - strtotime ( $request_time ) > 3600 * 24 * 7) { // 1 Week
			show_error ( lang ( 'error_verify_link_timeout' ) );
		}
		
		$email = $reset_row ['email'];
		$this->user_model->update_user ( $user_id, array (
				'verified_email' => $email 
		) );
		$this->user_model->clear_reset_key ( $reset_key );
		
		$data ['title'] = 'Email Verified';
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'user/verification_email_success', $data );
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
				$data ['message'] = 'Internal Error: Failed to update DB.';
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Call back function for the email field validation
	 *
	 * @param string $email        	
	 * @return boolean
	 */
	public function email_check($email) {
		$user = $this->user_model->query_user ( array (
				'email' => $email 
		) );
		if ($user) {
			$this->form_validation->set_message ( 'email_check', lang ( 'error_email_used' ) );
			return FALSE;
		}
		return TRUE;
	}
	private function _update_user_app_login_time($user_id) {
		$this->user_model->update_user ( $user_id, array (
				'lastAppLoginTime' => date ( 'Y-m-d H:i:s' ) 
		) );
	}
}

?>
