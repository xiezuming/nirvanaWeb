<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'call_script' )) {
	function call_script($script_file, $input) {
		$cmd = SCRIPT_PATH . "/$script_file " . escapeshellarg ( json_encode ( $input ) );
		log_message ( 'debug', "call_script: $cmd" );
		$result = shell_exec ( 'python ' . $cmd );
		
		log_message ( 'debug', "call_script raw result: $result" );
		
		$pos = stripos ( $result, PYTHON_PLACEHOLD );
		if ($pos) {
			$result = substr ( $result, $pos + strlen ( PYTHON_PLACEHOLD ) );
			$result = json_decode ( $result, true );
		}
		return $result;
	}
}