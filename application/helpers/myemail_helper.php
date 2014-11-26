<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'send_email' )) {
	/**
	 *
	 * @param string $from        	
	 * @param string $to        	
	 * @param string $subject        	
	 * @param string $email_body        	
	 * @return boolean TRUE if send successfully.
	 */
	function send_email($from, $to, $subject, $email_body) {
		$CI = & get_instance ();
		if (! $from)
			$from = 'Weee! Automated message do not reply <noreply@letustag.com>';
		if (! $to)
			$to = $CI->config->config ['mail'] ['report_address'];
		
		$fields = array (
				'from' => $from,
				'to' => $to,
				'subject' => $subject,
				'html' => $email_body 
		);
		if (SKIP_EMAIL) {
			log_message ( 'debug', 'Skip email sending for development. email fields:' . print_r ( $fields, true ) );
			return;
		}
		$result = TRUE;
		$ch = curl_init (); // initiate curl
		$url = $CI->config->config ['mail'] ['api_url']; // where you want to post data
		curl_setopt ( $ch, CURLOPT_URL, $url );
		curl_setopt ( $ch, CURLOPT_USERPWD, $CI->config->config ['mail'] ['user_pwd'] );
		// curl_setopt ( $ch, CURLOPT_HEADER, true );
		curl_setopt ( $ch, CURLOPT_POST, true ); // tell curl you want to post something
		curl_setopt ( $ch, CURLOPT_POSTFIELDS, http_build_query ( $fields ) ); // define what you want to post
		curl_setopt ( $ch, CURLOPT_RETURNTRANSFER, true ); // return the output in string format
		$output = curl_exec ( $ch ); // execute
		if (curl_errno ( $ch )) {
			log_message ( 'error', 'Faild to call email api: ' . print_r ( curl_getinfo ( $ch ), TRUE ) );
			$result = FALSE;
		}
		curl_close ( $ch ); // close curl handle
		log_message ( 'debug', 'email api output: ' . print_r ( $output, TRUE ) );
		
		return $result;
	}
}
