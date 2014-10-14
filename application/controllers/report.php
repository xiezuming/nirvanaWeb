<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

/**
 *
 * @property Report_model $report_model
 * @property User_model $user_model
 * @property Item_model $item_model
 */
class Report extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'report_model' );
		$this->load->model ( 'user_model' );
		$this->load->model ( 'item_model' );
	}
	public function index($report_id) {
		$report = $this->report_model->get_report ( $report_id );
		if (! $report) {
			show_404 ();
			return;
		}
		
		$data ['report'] = $report;
		$data ['report_user'] = $this->user_model->get_user ( $report ['reportUserId'] );
		$data ['report_item'] = $this->item_model->get_item ( $report ['itemId'] );
		
		$data ['title'] = 'Item Report';
		$this->load->helper ( 'view' );
		$this->load->view ( 'templates/header', $data );
		$this->load->view ( 'report/index', $data );
		$this->load->view ( 'templates/footer', $data );
	}
	public function report_item() {
		$report_id = $this->report_model->add_report ( $this->input->post () );
		if ($report_id) {
			$data ['result'] = SUCCESS;
			// send the email to the administrator
			$this->load->helper ( 'myemail' );
			$this->load->helper ( 'url' );
			$email_to = $this->config->config ['mail'] ['report_address'];
			$email_subject = "Somebody reported a item";
			$email_body = "New report: " . anchor ( "report/index/$report_id", 'View' );
			send_email ( '', $email_to, $email_subject, $email_body );
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'DB Error';
		}
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
}

?>
