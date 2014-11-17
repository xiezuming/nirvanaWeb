<?php
class User_model extends CI_Model {
	const TABLE_USER = 'user';
	const TABLE_GROUP = 'user_group';
	const TABLE_RESET = 'user_reset';
	public function create_user($data) {
		$user_id = $this->gen_uuid ();
		$user = array (
				'userId' => $user_id,
				'userType' => $data ['userType'],
				'password' => empty ( $data ['password'] ) ? '' : md5 ( $data ['password'] ),
				'alias' => $data ['alias'],
				'firstName' => $data ['firstName'],
				'lastName' => $data ['lastName'],
				'email' => empty ( $data ['email'] ) ? '' : $data ['email'],
				'fbUserId' => empty ( $data ['fbUserId'] ) ? '' : $data ['fbUserId'],
				'phoneNumber' => empty ( $data ['phoneNumber'] ) ? '' : $data ['phoneNumber'],
				'wechatId' => empty ( $data ['wechatId'] ) ? '' : $data ['wechatId'],
				'zipcode' => empty ( $data ['zipcode'] ) ? '' : $data ['zipcode'],
				'wxOpenId' => empty ( $data ['wxOpenId'] ) ? '' : $data ['wxOpenId'],
				'wxUnionId' => empty ( $data ['wxUnionId'] ) ? '' : $data ['wxUnionId'],
				'headImgUrl' => empty ( $data ['headImgUrl'] ) ? '' : $data ['headImgUrl'] 
		);
		$this->db->insert ( self::TABLE_USER, $user );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.create_user: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return $user_id;
		}
	}
	public function update_user($user_id, $data) {
		log_message ( 'debug', 'User_model.update_user: ' . $user_id );
		$this->db->where ( 'userId', $user_id );
		$this->db->update ( self::TABLE_USER, $data );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.update_user: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
	public function query_all_users() {
		$query = $this->db->get ( self::TABLE_USER );
		$result = $query->result_array ();
		return $result;
	}
	public function get_user($userId) {
		$where = array (
				'userId' => $userId 
		);
		$query = $this->db->get_where ( self::TABLE_USER, $where );
		$user = $query->row_array ();
		return $user;
	}
	public function query_user_by_email($email) {
		$where = array (
				'email' => $email 
		);
		$query = $this->db->get_where ( self::TABLE_USER, $where );
		$user = $query->row_array ();
		return $user;
	}
	public function query_user($where) {
		$query = $this->db->get_where ( self::TABLE_USER, $where );
		$user = $query->row_array ();
		return $user;
	}
	public function reset_password($user_id, $password) {
		$this->db->where ( 'userId', $user_id );
		$this->db->update ( self::TABLE_USER, array (
				'password' => md5 ( $password ) 
		) );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.reset_password: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
	/* Wish List *************** */
	public function update_wish_list($user_id, $wish_list) {
		$this->db->where ( 'userId', $user_id );
		$this->db->update ( self::TABLE_USER, array (
				'wishList' => $wish_list 
		) );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.update_wish_list: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
	/* Password Reset *************** */
	public function create_reset_key($userId, $email = NULL) {
		$reset_key = $this->gen_uuid ();
		$date = array (
				'userId' => $userId,
				'reset_key' => $reset_key,
				'email' => $email 
		);
		$this->db->insert ( self::TABLE_RESET, $date );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.create_reset: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return $reset_key;
		}
	}
	public function get_reset_row($reset_key) {
		$query = $this->db->get_where ( self::TABLE_RESET, array (
				'reset_key' => $reset_key 
		) );
		$reset_row = $query->row_array ();
		return $reset_row;
	}
	public function clear_reset_key($reset_key) {
		$this->db->where ( 'reset_key', $reset_key );
		$this->db->update ( self::TABLE_RESET, array (
				'key_used' => 'Y' 
		) );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.clear_reset_key: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
	/* User Group *************** */
	public function get_user_groups($user_id) {
		return $this->db->get_where ( self::TABLE_GROUP, array (
				'user_id' => $user_id 
		) )->result_array ();
	}
	public function update_user_group($user_id, $user_groups) {
		$this->db->delete ( self::TABLE_GROUP, array (
				'user_id' => $user_id 
		) );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.update_user_group: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		}
		
		if (! $user_groups)
			return TRUE;
		
		$user_group_rows = array ();
		foreach ( $user_groups as $user_group ) {
			array_push ( $user_group_rows, array (
					'user_id' => $user_id,
					'group_key' => $user_group 
			) );
		}
		
		$this->db->insert_batch ( self::TABLE_GROUP, $user_group_rows );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'User_model.update_user_group: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
	/* Private Functions *************** */
	private function rand_string($length) {
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