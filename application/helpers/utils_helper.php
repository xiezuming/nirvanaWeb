<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'output_json_result' )) {
	function output_json_result($result, $message = NULL, $object = NULL) {
		$data ['result'] = $result;
		$data ['message'] = $message;
		$data ['object'] = $object;
		$CI = & get_instance ();
		if (! error_get_last ()) {
			$CI->output->set_content_type ( 'application/json' );
		}
		$CI->output->set_output ( json_encode ( $data ) );
	}
}
