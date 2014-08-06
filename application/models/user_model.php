<?php
class User_model extends CI_Model {
	const TABLE_USER = 'user';
	public function create_user($data) {
		$user = array (
				'userId' => $this->gen_uuid (),
				'userName' => $data ['userName'],
				'password' => md5 ( $data ['password'] ),
				'firstName' => $data ['firstName'],
				'lastName' => $data ['lastName'],
				'phoneNumber' => $data ['phoneNumber'],
				'wechatId' => $data ['wechatId'] 
		);
		$this->db->insert ( self::TABLE_USER, $user );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.create_user: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
	public function get_user($userId) {
		$where = array (
				'userId' => $userId 
		);
		$query = $this->db->get_where ( self::TABLE_USER, $where );
		$user = $query->row_array ();
		return $user;
	}
	public function query_user($userName) {
		$where = array (
				'userName' => $userName 
		);
		$query = $this->db->get_where ( self::TABLE_USER, $where );
		$user = $query->row_array ();
		return $user;
	}
	public function login($userName, $password) {
		$where = array (
				'userName' => $userName,
				'password' => md5 ( $password ) 
		);
		$query = $this->db->get_where ( self::TABLE_USER, $where );
		$user = $query->row_array ();
		if ($user) {
			$data ['userId'] = $user ['userId'];
			return $data;
		}
		return NULL;
	}
	public function logout($userId) {
		$data = array (
				'token' => NULL 
		);
		$this->db->where ( 'userId', $userId );
		$this->db->update ( self::TABLE_USER, $data );
	}
	public function check_user($userId, $token) {
		$where = array (
				'userId' => $userId,
				'token' => $token 
		);
		$query = $this->db->get_where ( self::TABLE_USER, $where );
		
		return ($query->row_array () == NULL);
	}
	function rand_string($length) {
		$chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789";
		
		$size = strlen ( $chars );
		$str = '';
		for($i = 0; $i < $length; $i ++) {
			$str .= $chars [rand ( 0, $size - 1 )];
		}
		
		return $str;
	}
	private function gen_uuid() {
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
?>