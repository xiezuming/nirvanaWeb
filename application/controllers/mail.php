<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

/**
 *
 * @property User_model $user_model
 */
class Mail extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'user_model' );
	}
	function index() {
		log_message ( 'debug', 'Mail.index: post = ' . print_r ( $this->input->post (), true ) );
	}
}