<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const GROUP_TYPE_ID = 5;

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
		$this->form_validation->set_rules ( 'user_groups', 'Group', '' );
		
		if ($this->form_validation->run ()) {
			$input_data = $this->input->post ();
			$input_data ['userType'] = USER_TYPE_WETAG;
			$input_data ['alias'] = $input_data ['firstName'];
			$user_id = $this->user_model->create_user ( $input_data );
			$user_groups = $this->input->post ( 'user_groups' );
			if ($user_id && $this->user_model->update_user_group ( $user_id, $user_groups )) {
				$this->load->view ( 'user/jump_sign_up_success' );
				return;
			} else {
				echo "DB ERROR.";
				return;
			}
		}
		
		$data ['group_array'] = $this->get_all_group_array ();
		$data ['title'] = 'Sign Up';
		$this->load->view ( 'templates/header_app', $data );
		$this->load->view ( 'user/sign_up', $data );
		$this->load->view ( 'templates/footer_app' );
	}
	public function edit_profile($user_id = '') {
		$this->load->helper ( 'form' );
		
		if (! $user_id) {
			$user_id = $this->input->post ( 'userId' );
			if (! $user_id)
				show_error ( 'Invalid user id.' );
		}
		
		// init load
		$data ['user'] = $this->user_model->get_user ( $user_id );
		if (! $data ['user']) {
			show_error ( 'Invalid user.' );
		}
		$data ['user'] ['user_groups'] = $this->get_user_group_key_array ( $user_id );
		
		if ($this->input->post ()) {
			$this->load->library ( 'form_validation' );
			$this->form_validation->set_rules ( 'firstName', 'First Name', 'required|max_length[45]' );
			$this->form_validation->set_rules ( 'lastName', 'Last Name', 'required|max_length[45]' );
			$this->form_validation->set_rules ( 'alias', 'Alias', 'required|max_length[45]' );
			$this->form_validation->set_rules ( 'email', 'Email Address', 'required|valid_email|max_length[45]|callback_email_check[' . $data ['user'] ['userId'] . ',' . $data ['user'] ['userType'] . ']' );
			$this->form_validation->set_rules ( 'password', 'Password', 'matches[password_confirm]' );
			$this->form_validation->set_rules ( 'password_confirm', 'Password Confirmation', '' );
			$this->form_validation->set_rules ( 'zipcode', 'ZIP Code', 'required|max_length[10]' );
			$this->form_validation->set_rules ( 'phoneNumber', 'Phone Number', 'max_length[45]' );
			$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', 'max_length[45]' );
			$this->form_validation->set_rules ( 'user_groups', 'Group', '' );
			
			if ($this->form_validation->run ()) {
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
				
				$user_groups = $this->input->post ( 'user_groups' );
				if ($success && $this->user_model->update_user_group ( $user_id, $user_groups )) {
					$this->session->set_flashdata ( 'falshmsg', array (
							'type' => 'message',
							'content' => 'Update successfully.' 
					) );
					redirect ( site_url ( "/user/edit_profile/" . $user_id ), 'refresh' );
				} else {
					echo "DB ERROR.";
					return;
				}
			}
			$data ['userId'] = $user_id;
		}
		
		$data ['group_array'] = $this->get_all_group_array ();
		$data ['title'] = 'Edit Profile';
		$this->load->view ( 'templates/header_app', $data );
		$this->load->view ( 'user/edit_profile', $data );
		$this->load->view ( 'templates/footer_app' );
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
		$this->form_validation->set_rules ( 'email', 'Email Address', 'required|valid_email|max_length[45]|callback_email_check[' . $user ['userId'] . ',' . $user ['userType'] . ']' );
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
			$data ['result'] = SUCCESS;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Failed to update the database.';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function sign_up_success() {
		echo "SUCCESS";
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
					'email' => $email,
					'userType' => USER_TYPE_WETAG 
			) );
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
				$data ['message'] = 'That Weee! account doesn\'t exist. Enter a different email address or get a new account';
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
				$data ['result'] = SUCCESS;
				$user ['password'] = '';
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
				$user_id = $this->user_model->create_user ( $input_data );
				if (! $user_id) {
					$data ['result'] = FAILURE;
					$data ['message'] = 'Internal Error: Falied to crate the user.';
				}
			}
			if ($user_id) {
				$data ['result'] = SUCCESS;
				$user ['password'] = '';
				$data ['data'] = $this->user_model->get_user ( $user_id );
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
			
			$user = $this->user_model->query_user ( $where = array (
					'email' => $email_address,
					'userType' => USER_TYPE_WETAG 
			) );
			
			if ($user) {
				$user_id = $user ['userId'];
				$reset_key = $this->user_model->create_reset_key ( $user_id );
				if ($reset_key) {
					$link = site_url ( 'user/reset_password/' . $user_id . '/' . $reset_key );
					$result = $this->send_reset_password_email ( $email_address, $link );
					if ($result) {
						$data ['result'] = SUCCESS;
						$data ['message'] = 'Instructions on how to reset your password have been sent to ' . $email_address . '.';
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
	public function email_check($email, $params = '') {
		$params = explode ( ',', $params );
		$user_id = empty ( $params [0] ) ? '' : $params [0];
		$user_type = empty ( $params [1] ) ? USER_TYPE_WETAG : $params [1];
		log_message ( 'debug', '------------' . $email . ',' . $user_id . ',' . $user_type );
		$user = $this->user_model->query_user ( array (
				'email' => $email,
				'userType' => $user_type,
				'userId !=' => $user_id 
		) );
		if ($user) {
			$this->form_validation->set_message ( 'email_check', 'Email Address is registered by another account.' );
			return FALSE;
		}
		return TRUE;
	}
	private function send_reset_password_email($email, $link) {
		$fields = array (
				'from' => 'Weee! Automated message do not reply <robot@letustag.com>',
				'to' => $email,
				'subject' => '[Weee!] How to reset your password',
				'html' => $this->load->view ( 'user/reset_password_mail', array (
						'link' => $link 
				), TRUE ) 
		);
		
		$ch = curl_init (); // initiate curl
		$url = $this->config->config ['mail'] ['api_url']; // where you want to post data
		curl_setopt ( $ch, CURLOPT_URL, $url );
		curl_setopt ( $ch, CURLOPT_USERPWD, $this->config->config ['mail'] ['user_pwd'] );
		// curl_setopt ( $ch, CURLOPT_HEADER, true );
		curl_setopt ( $ch, CURLOPT_POST, true ); // tell curl you want to post something
		curl_setopt ( $ch, CURLOPT_POSTFIELDS, http_build_query ( $fields ) ); // define what you want to post
		curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true ); // return the output in string format
		$output = curl_exec ( $ch ); // execute
		if (curl_errno ( $ch )) {
			log_message ( 'error', 'Faild to call email api: ' . print_r ( curl_getinfo ( $ch ), TRUE ) );
			return FALSE;
		}
		curl_close ( $ch ); // close curl handle
		log_message ( 'debug', 'email api output: ' . print_r ( $output, TRUE ) );
		return TRUE;
	}
	private function get_user_group_key_array($user_id) {
		$user_group_key_array = array ();
		foreach ( $this->user_model->get_user_groups ( $user_id ) as $user_group_row )
			array_push ( $user_group_key_array, $user_group_row ['group_key'] );
		return $user_group_key_array;
	}
	private function get_all_group_array() {
		$this->load->model ( 'meta_model' );
		return $this->meta_model->get_meta_codes ( GROUP_TYPE_ID );
	}
}

?>
