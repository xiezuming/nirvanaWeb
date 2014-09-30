<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'gen_uuid' )) {
	function gen_uuid() {
		return sprintf ( '%04x%04x-%04x-%04x-%04x-%04x%04x%04x', 
				// 32 bits for "time_low"
				mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), 
				
				// 16 bits for "time_mid"
				mt_rand ( 0, 0xffff ), 
				
				// 16 bits for "time_hi_and_version",
				// four most significant bits holds version number 4
				mt_rand ( 0, 0x0fff ) | 0x4000, 
				
				// 16 bits, 8 bits for "clk_seq_hi_res",
				// 8 bits for "clk_seq_low",
				// two most significant bits holds zero and one for variant DCE1.1
				mt_rand ( 0, 0x3fff ) | 0x8000, 
				
				// 48 bits for "node"
				mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ), mt_rand ( 0, 0xffff ) );
	}
}
if (! function_exists ( 'encode_uuid_base64' )) {
	function encode_uuid_base64($uuid) {
		$byteString = "";
		
		// Remove the dashes from the string
		$uuid = str_replace ( "-", "", $uuid );
		
		// Read the UUID string byte by byte
		for($i = 0; $i < strlen ( $uuid ); $i += 2) {
			// Get two hexadecimal characters
			$s = substr ( $uuid, $i, 2 );
			// Convert them to a byte
			$d = hexdec ( $s );
			// Convert it to a single character
			$c = chr ( $d );
			// Append it to the byte string
			$byteString = $byteString . $c;
		}
		
		// Convert the byte string to a base64 string
		$b64uuid = base64_encode ( $byteString );
		// Replace the "/" and "+" since they are reserved characters
		$b64uuid = strtr ( $b64uuid, '+/', '-_' );
		// Remove the trailing "=="
		$b64uuid = substr ( $b64uuid, 0, strlen ( $b64uuid ) - 2 );
		
		return $b64uuid;
	}
}
if (! function_exists ( 'decode_uuid_base64' )) {
	function decode_uuid_base64($b64uuid) {
		$b64uuid .= '==';
		$b64uuid = strtr ( $b64uuid, '-_', '+/' );
		$byteString = base64_decode ( $b64uuid );
		
		$uuid = "";
		for($i = 0; $i < strlen ( $byteString ); $i ++) {
			// Get a single character
			$c = substr ( $byteString, $i, 1 );
			// Convert it to a byte
			$d = ord ( $c );
			// Convert it to hexadecimal characters
			$s = str_pad ( dechex ( $d ), 2, '0', STR_PAD_LEFT );
			// Append it to the uuid string
			$uuid .= $s;
		}
		
		// Add dashes
		$uuid = substr_replace ( $uuid, '-', 8, 0 );
		$uuid = substr_replace ( $uuid, '-', 13, 0 );
		$uuid = substr_replace ( $uuid, '-', 18, 0 );
		$uuid = substr_replace ( $uuid, '-', 23, 0 );
		
		return $uuid;
	}
}