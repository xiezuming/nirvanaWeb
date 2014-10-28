<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'send_notification' )) {
	
	/**
	 * Get the location related information by zipcode
	 *
	 * @param string $zipcode        	
	 * @return The location array containing region and geometry information
	 */
	
	/**
	 * Send the push notification to the user
	 *
	 * @param string $user_id        	
	 * @param string $message        	
	 * @return boolean
	 */
	function send_notification($user_id, $message) {
		$data = array (
				"where" => array (
						"userId" => $user_id 
				),
				"data" => array (
						"alert" => $message 
				) 
		);
		$data_string = json_encode ( $data );
		
		$CI = & get_instance ();
		$appid = $CI->config->config ['parse'] ['appid'];
		$key = $CI->config->config ['parse'] ['key'];
		
		$url = "https://api.parse.com/1/push";
		$ch = curl_init ( $url );
		curl_setopt ( $ch, CURLOPT_CUSTOMREQUEST, "POST" );
		curl_setopt ( $ch, CURLOPT_POSTFIELDS, $data_string );
		curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true );
		curl_setopt ( $ch, CURLOPT_HTTPHEADER, array (
				'Content-Type: application/json',
				"X-Parse-Application-Id: $appid",
				"X-Parse-REST-API-Key: $key" 
		) );
		
		$ret_json = curl_exec ( $ch );
		if (curl_errno ( $ch )) {
			log_message ( 'error', 'Faild to call Parse Push api: ' . print_r ( curl_getinfo ( $ch ), TRUE ) );
			curl_close ( $ch ); // close curl handle
			return FALSE;
		}
		curl_close ( $ch ); // close curl handle
		
		$ret = json_decode ( $ret_json, true );
		if (! $ret) {
			log_message ( 'error', 'Faild to parse the Parse Push api response: ' . print_r ( $ret_json, TRUE ) );
			return FALSE;
		}
		
		$status = array_key_exists ( 'status', $result ) ? $ret ['status'] : 'ERROR';
		if ($status != true) {
			log_message ( 'error', "The status in the Parse Push api response is not OK: ${status}. json = $ret_json" );
			return FALSE;
		}
		
		return TRUE;
	}
}

