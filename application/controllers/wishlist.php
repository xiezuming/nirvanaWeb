<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

/**
 *
 * @property Wishlist_model $wishlist_model
 * @property User_model $user_model
 * @property Activity_model $activity_model
 */
class Wishlist extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'wishlist_model' );
		$this->load->model ( 'user_model' );
		$this->load->model ( 'activity_model' );
	}
	function index($activity_id = 0) {
		$activity = $this->activity_model->get_activity ( $activity_id );
		if (! $activity) {
			show_404 ();
			return;
		}
		
		$wishlist_rows = $this->wishlist_model->query_published_wishlist ( $activity_id );
		$data ['title'] = 'Wish List';
		$data ['activity'] = $activity;
		
		$wishlist_array = array ();
		foreach ( $wishlist_rows as $wishlist ) {
			$contact_info = "Email: ${wishlist['email']}<br/>";
			if ($wishlist ['wechatId'])
				$contact_info .= "WeChat ID: ${wishlist['wechatId']}<br/>";
			if ($wishlist ['zipcode'])
				$contact_info .= "ZIP Code: ${wishlist['zipcode']}<br/>";
			$wishlist ['contact_info'] = $contact_info;
			array_push ( $wishlist_array, $wishlist );
		}
		$data ['wishlist_array'] = $wishlist_array;
		
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'wishlist/index', $data );
		$this->load->view ( 'templates/footer', $data );
	}
	function add_wishlist($activity_id = 0) {
		$activity = $this->activity_model->get_activity ( $activity_id );
		if (! $activity) {
			show_404 ();
			return;
		}
		
		$data ['title'] = 'Submit Your Wish List';
		$data ['activity'] = $activity;
		
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		$this->form_validation->set_rules ( 'email', 'Email', 'required||max_length[45]|valid_email' );
		$this->form_validation->set_rules ( 'wishlist_text', 'Title', 'required' );
		$this->form_validation->set_rules ( 'price_min', 'Price Min', 'numeric' );
		$this->form_validation->set_rules ( 'price_max', 'Price Max', 'numeric' );
		$this->form_validation->set_rules ( 'wechatId', 'WeChat ID', '' );
		$this->form_validation->set_rules ( 'zipcode', 'ZIP Code', '' );
		
		if (! $this->form_validation->run ()) {
			$data ['error'] = '';
			$this->form_validation->set_error_delimiters ( '<p style="color:red">', '</p>' );
			return $this->load_add_wishlist_view ( $data );
		}
		
		// get the user by email. create it if not exist.
		$user = $this->create_user ();
		if (! $user) {
			$data ['error'] = 'Internal Error: failed to create the user.';
			return $this->load_add_wishlist_view ( $data );
		}
		
		// save the item and his activity relation into the DB
		$this->load->helper ( 'uuid' );
		$wishlist_uuid = gen_uuid ();
		$wishlist_text = $this->input->post ( 'wishlist_text' );
		$price_min = $this->input->post ( 'price_min' ) ? $this->input->post ( 'price_min' ) : NULL;
		$price_max = $this->input->post ( 'price_max' ) ? $this->input->post ( 'price_max' ) : NULL;
		$email = $this->input->post ( 'email' );
		$wechatId = $this->input->post ( 'wechatId' ) ? $this->input->post ( 'wechatId' ) : NULL;
		$zipcode = $this->input->post ( 'zipcode' ) ? $this->input->post ( 'zipcode' ) : NULL;
		$result = $this->wishlist_model->add_wishlist ( array (
				'wishlist_uuid' => $wishlist_uuid,
				'activity_id' => $activity_id,
				'wishlist_text' => $wishlist_text,
				'price_min' => $price_min,
				'price_max' => $price_max,
				'user_id' => $user ['userId'],
				'email' => $email,
				'wechatId' => $wechatId,
				'zipcode' => $zipcode 
		) );
		if (! $result) {
			log_message ( 'error', 'Wishlist.add_wishlist: Failed to update the database.' );
			$data ['error'] = 'Failed to update the database.';
			return $this->load_add_wishlist_view ( $data );
		}
		
		// send the email
		$this->load->helper ( 'myemail' );
		$email_subject = "POST WISH LIST ITEM: \"$wishlist_text\"";
		$email_body = $this->load->view ( 'wishlist/add_wishlist_success_message_body', array (
				'wishlist_uuid' => encode_uuid_base64 ( $wishlist_uuid ) 
		), TRUE );
		send_email ( '', $user ['email'], $email_subject, $email_body );
		
		$data ['title'] = 'Success - Submit Your Wish List';
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'wishlist/add_wishlist_success', $data );
		$this->load->view ( 'templates/footer', $data );
	}
	private function load_add_wishlist_view($data) {
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'wishlist/add_wishlist', $data );
		$this->load->view ( 'templates/footer', $data );
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
	public function activate_wishlist($b64_wishlist_uuid = 0) {
		$this->load->helper ( 'uuid' );
		$wishlist_uuid = decode_uuid_base64 ( $b64_wishlist_uuid );
		$wishlist = $this->wishlist_model->query_wishlist_by_uuid ( $wishlist_uuid );
		if (! $wishlist) {
			show_error ( 'Invalid URL' );
			return;
		}
		
		$this->wishlist_model->update_wishlist ( $wishlist_uuid, array (
				'published' => 'Y' 
		) );
		
		$data ['title'] = 'Success - Publish Your Item';
		$data ['wishlist'] = $wishlist;
		
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'wishlist/activate_wishlist_success', $data );
		$this->load->view ( 'templates/footer', $data );
	}
}

?>
