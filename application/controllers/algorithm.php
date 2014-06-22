<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;
const PYTHON_PLACEHOLD = '***|||RESULT|||***';
/**
 */
class Algorithm extends CI_Controller {
	function __construct() {
		parent::__construct ();
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->view ( 'algorithm/test_form' );
	}
	public function query_item_defaults_by_barcode() {
		$barcode = $this->input->post ( 'barcode' );
		if (empty ( $barcode )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Barcode is empty.';
		} else {
			$input = array (
					$barcode 
			);
			$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'query_item_defaults_by_barcode.py';
			$result = shell_exec ( 'python ' . $cmd . ' ' . escapeshellarg ( json_encode ( $input ) ) );
			$result = $this->get_real_result ( $result );
			if (empty ( $result )) {
				$data ['result'] = FAILURE;
				$data ['message'] = 'No result found for barcode.';
			} else {
				$data ['result'] = SUCCESS;
				$data ['data'] = array (
						'item_defaults' => $result 
				);
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	private function get_real_result($result) {
		$pos = stripos ( $result, PYTHON_PLACEHOLD );
		if ($pos) {
			$result = substr ( $result, $pos + strlen ( PYTHON_PLACEHOLD ) );
			$result = json_decode ( $result, true );
		}
		return $result;
	}
}

?>
