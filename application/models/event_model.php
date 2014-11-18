<?php
class Event_model extends CI_Model {
	const TABLE_EVENT = 'event';
	public function get_events_where($where) {
		$this->db->order_by ( 'event_create_time', 'desc' );
		return $this->db->get_where ( self::TABLE_EVENT, $where )->result_array ();
	}
	public function get_event($event_id) {
		$this->db->where ( 'event_id', $event_id );
		return $this->db->get ( self::TABLE_EVENT )->row_array ();
	}
	public function add_event($data) {
		$user = array (
				'user_id' => $data ['user_id'],
				'event_type' => $data ['event_type'],
				'event_sub_type' => $data ['event_sub_type'],
				'event_text' => $data ['event_text'] 
		);
		$this->db->insert ( self::TABLE_EVENT, $user );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'Event_model.add_event: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return $this->db->insert_id ();
		}
	}
	public function mark_event_finished($event_id) {
		$this->db->where ( 'event_id', $event_id );
		$result = $this->db->update ( self::TABLE_EVENT, array (
				'event_finished' => 'Y' 
		) );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Event_model.mark_event_finished: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
}
?>