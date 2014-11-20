<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
	
	/*
 * |--------------------------------------------------------------------------
 * | File and Directory Modes
 * |--------------------------------------------------------------------------
 * |
 * | These prefs are used when checking and setting modes when working
 * | with the file system. The defaults are fine on servers with proper
 * | security, but you may wish (or even need) to change the values in
 * | certain environments (Apache running a separate process for each
 * | user, PHP under CGI with Apache suEXEC, etc.). Octal values should
 * | always be used to set the mode correctly.
 * |
 */
define ( 'FILE_READ_MODE', 0644 );
define ( 'FILE_WRITE_MODE', 0666 );
define ( 'DIR_READ_MODE', 0755 );
define ( 'DIR_WRITE_MODE', 0777 );

/*
 * |--------------------------------------------------------------------------
 * | File Stream Modes
 * |--------------------------------------------------------------------------
 * |
 * | These modes are used when working with fopen()/popen()
 * |
 */

define ( 'FOPEN_READ', 'rb' );
define ( 'FOPEN_READ_WRITE', 'r+b' );
define ( 'FOPEN_WRITE_CREATE_DESTRUCTIVE', 'wb' ); // truncates existing file data, use with care
define ( 'FOPEN_READ_WRITE_CREATE_DESTRUCTIVE', 'w+b' ); // truncates existing file data, use with care
define ( 'FOPEN_WRITE_CREATE', 'ab' );
define ( 'FOPEN_READ_WRITE_CREATE', 'a+b' );
define ( 'FOPEN_WRITE_CREATE_STRICT', 'xb' );
define ( 'FOPEN_READ_WRITE_CREATE_STRICT', 'x+b' );

define ( 'SUCCESS', 1 );
define ( 'FAILURE', 0 );
define ( 'USER_TYPE_WETAG', 'WE' );
define ( 'USER_TYPE_FACEBOOK', 'FB' );
define ( 'USER_TYPE_WEIXIN', 'WX' );

define ( 'LOG_BASE_PATH', '/var/log/weee_app/' );
define ( 'UPLOAD_BASE_PATH', '/var/uploads/weee_app/' );
define ( 'SCRIPT_PATH', '/home/ubuntu/project/weee_algo/scripts/' );

define ( 'META_TYPE_CONDITION', 2 );
define ( 'OFTEN_SELL_TO_US', 10 ); // TODO for test, 3600 * 24 * 7
define ( 'OFTEN_DONATE', 10 ); // TODO for test, 3600 * 24 * 30

define ( 'PYTHON_PLACEHOLD', '***|||RESULT|||***' );

define ( 'PUSH_TYPE_ALERT_MESSAGE', 'a' );

/* End of file constants.php */
/* Location: ./application/config/constants.php */
