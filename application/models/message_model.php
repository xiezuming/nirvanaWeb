<?php
class Message_model extends CI_Model {
	const TABLE_MESSAGE = 'message';
	public function query_messages($where, $limit, $offset) {
		$this->db->select ( '
				messageUuid, 
				fromUserId, 
				fromUserName, 
				toUserId, 
				toUserName, 
				itemUuid, 
				itemUserId, 
				itemTitle, 
				itemImageName, 
				message, 
				isRead,
				UNIX_TIMESTAMP(recCreateTime) as recCreateTime' );
		$this->db->order_by ( 'recCreateTime', 'asc' );
		$query = $this->db->get_where ( self::TABLE_MESSAGE, $where, $limit, $offset );
		log_message ( 'debug', "Message_model.query_messages: SQL = \n" . $this->db->last_query () );
		return $query->result_array ();
	}
	public function add_message($message) {
		$this->db->insert ( self::TABLE_MESSAGE, $message );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'Message_model.add_message: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
	public function mark_message_read($where) {
		$this->db->where ( $where );
		$this->db->update ( self::TABLE_MESSAGE, array (
				'isRead' => 'Y' 
		) );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'Message_model.mark_message_read: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return TRUE;
		}
	}
}
?>