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
	public function query_item_prices() {
		$barcode = $this->input->post ( 'barcode' );
		$title = $this->input->post ( 'title' );
		if (empty ( $barcode ) && empty ( $title )) {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: The inputs is empty.';
		} else {
			$input = array (
					$barcode,
					$title 
			);
			$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'query_item_prices.py';
			$result = shell_exec ( 'python ' . $cmd . ' ' . escapeshellarg ( json_encode ( $input ) ) );
			$result = $this->get_real_result ( $result );
			if (empty ( $result )) {
				$data ['result'] = FAILURE;
				$data ['message'] = 'No result found for barcode.';
			} else {
				$data ['result'] = SUCCESS;
				$data ['data'] = array (
						'item_prices' => $result 
				);
			}
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function query_categories_by_title() {
		$title = $this->input->post ( 'title' );
		if (empty ( $title )) {
			show_error ( 'Title is empty.' );
			return;
		} else {
			$input = array (
					$title 
			);
			$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'query_categories_by_title.py';
			$result = shell_exec ( 'python ' . $cmd . ' ' . escapeshellarg ( json_encode ( $input ) ) );
			$categories = $this->get_real_result ( $result );
			
			$data ['title'] = 'Step 1/2: Category List';
			$data ['query_title'] = $title;
			$data ['categories'] = $categories;
			
			$this->load->helper ( 'form' );
			$this->load->view ( 'templates/header_app', $data );
			$this->load->view ( 'algorithm/categories', $data );
			$this->load->view ( 'templates/footer_app' );
		}
		// $this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function query_similar_itmes() {
		$catNum = $this->input->post ( 'catNum' );
		$title = $this->input->post ( 'title' );
		if (empty ( $catNum )) {
			show_error ( 'Category number is empty.' );
			return;
		} else {
			$input = array (
					$title,
					$catNum 
			);
			$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'query_similar_itmes.py';
			$result = shell_exec ( 'python ' . $cmd . ' ' . escapeshellarg ( json_encode ( $input ) ) );
			$items = $this->get_real_result ( $result );
			
			$data ['title'] = 'Step 2/2: Item List';
			$data ['items'] = $items;
			
			$this->load->helper ( 'form' );
			$this->load->view ( 'templates/header_app', $data );
			$this->load->view ( 'algorithm/items', $data );
			$this->load->view ( 'templates/footer_app' );
		}
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
