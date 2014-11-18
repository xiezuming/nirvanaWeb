<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

/**
 *
 * @property Event_model $event_model
 * @property User_model $user_model
 */
class Event extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'event_model' );
		$this->load->model ( 'user_model' );
		$this->load->helper ( 'myemail' );
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'event/test_form', $data );
	}
	public function index($event_id) {
		$event = $this->event_model->get_event ( $event_id );
		if (! $event)
			show_404 ();
		$user = $this->user_model->get_user ( $event ['user_id'] );
		$user ['password'] = '********';
		
		$data ['title'] = 'View Event';
		$data ['event'] = $event;
		$data ['user'] = $user;
		
		$this->load->view ( 'templates/header_app', $data );
		$this->load->view ( 'event/index' );
		$this->load->view ( 'templates/footer_app' );
	}
	public function finish($event_id) {
		$event = $this->event_model->get_event ( $event_id );
		if (! $event)
			show_404 ();
		
		$this->event_model->mark_event_finished ( $event_id );
		redirect ( "event/index/$event_id", 'refresh' );
	}
	public function contact($user_id = '') {
		if (empty ( $user_id )) {
			$user_id = $this->input->post ( 'user_id' );
			if (empty ( $user_id ))
				show_error ( 'Invalid user.' );
		}
		
		$this->load->helper ( 'form' );
		$data ['title'] = 'Contact Us';
		if ($this->input->post ()) {
			$this->load->library ( 'form_validation' );
			$this->form_validation->set_rules ( 'event_sub_type', 'Subject', 'required|max_length[45]' );
			$this->form_validation->set_rules ( 'event_text', 'Body', 'required' );
			
			if ($this->form_validation->run ()) {
				$event_id = $this->event_model->add_event ( $this->get_input_data () );
				if ($event_id) {
					$this->_send_notification_email ( $event_id );
					
					$this->load->view ( 'templates/header_app', $data );
					$this->load->view ( 'event/contact_success' );
					$this->load->view ( 'templates/footer_app' );
					return;
				} else {
					show_error ( 'DB Error.' );
				}
			}
		}
		
		$data ['user_id'] = $user_id;
		$this->load->view ( 'templates/header_app', $data );
		$this->load->view ( 'event/contact', $data );
		$this->load->view ( 'templates/footer_app' );
	}
	public function add_event() {
		$success = $this->event_model->add_event ( $this->get_input_data () );
		if ($success) {
			$data ['result'] = SUCCESS;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'DB Error';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function contact_home() {
		$input ['user_id'] = $this->input->post ( 'name' );
		$input ['event_type'] = 'contact_home';
		$input ['event_sub_type'] = $this->input->post ( 'email' );
		$input ['event_text'] = $this->input->post ( 'message' );
		$success = $this->event_model->add_event ( $input );
		if ($success) {
			$data ['result'] = SUCCESS;
			$data ['message'] = 'SUCCESS';
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'DB Error';
		}
		$this->output->set_header ( 'Access-Control-Allow-origin: *' );
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function sell_to_wetag() {
		$input = $this->get_input_data ();
		$user_id = $input ['user_id'];
		$events = $this->event_model->get_events_where ( array (
				'user_id' => $user_id,
				'event_type' => 'sell_to_weee' 
		) );
		if (count ( $events ) > 0) {
			/*if (time () - strtotime ( $events [0] ['event_create_time'] ) < 3600 * 24 * 7) { // 7 days
				$data ['result'] = FAILURE;
				$data ['message'] = 'You can send the request only once a week.';
				$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
				return;
			}*/
		}
		$input ['event_type'] = 'sell_to_weee';
		$event_id = $this->event_model->add_event ( $input );
		if ($event_id) {
			$this->_send_notification_email ( $event_id );
			
			$user = $this->user_model->get_user ( $user_id );
			$data ['result'] = SUCCESS;
			$data ['message'] = 'We will email you our offer to your email at ' . $user ['email'] . ' within 24 hours';
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'DB Error';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function donate() {
		$input = $this->get_input_data ();
		$user_id = $input ['user_id'];
		$events = $this->event_model->get_events_where ( array (
				'user_id' => $user_id,
				'event_type' => 'donate' 
		) );
		if (count ( $events ) > 0) {
			/*if (time () - strtotime ( $events [0] ['event_create_time'] ) < 3600 * 24 * 30) { // 30 days
				$data ['result'] = FAILURE;
				$data ['message'] = 'You can send the request only once a month.';
				$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
				return;
			}*/
		}
		$input ['event_type'] = 'donate';
		$event_id = $this->event_model->add_event ( $input );
		if ($event_id) {
			$this->_send_notification_email ( $event_id );
			
			$data ['result'] = SUCCESS;
			$data ['message'] = 'We have received your donation request. We will connect you later.';
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'DB Error';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	private function get_field_names() {
		$field_names = array (
				"user_id" => "user_id",
				"event_type" => "event_type",
				"event_sub_type" => "event_sub_type",
				"event_text" => "event_text" 
		);
		return $field_names;
	}
	private function get_input_data() {
		log_message ( 'debug', 'input: ' . print_r ( $this->input->post (), TRUE ) );
		$input_data = array ();
		foreach ( $this->get_field_names () as $field_name ) {
			$field_value = $this->input->post ( $field_name );
			if (empty ( $field_value )) {
				$input_data [$field_name] = NULL;
			} else {
				// change
				if ($this->endsWith ( $field_name, 'Time' )) {
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
	private function _send_notification_email($event_id) {
		send_email ( null, null, '[Weee!] New Event', 'New Event.' . anchor ( "event/index/$event_id", 'View' ) );
	}
}

?>
