<?php
class Activity_model extends CI_Model {
	const TABLE_ACTIVITY = 'activity';
	const TABLE_ACTIVITY_ITEM = 'activity_item';
	public function get_activity($activity_id) {
		$this->db->where ( 'activity_id', $activity_id );
		$query = $this->db->get ( self::TABLE_ACTIVITY );
		return $query->row_array ();
	}
	public function get_activities_by_item($global_item_id) {
		$this->db->from ( self::TABLE_ACTIVITY );
		$this->db->join ( self::TABLE_ACTIVITY_ITEM, self::TABLE_ACTIVITY . '.Activity_ID = ' . self::TABLE_ACTIVITY_ITEM . '.Activity_ID' );
		$this->db->where ( 'Global_Item_ID', $global_item_id );
		$query = $this->db->get ();
		if ($this->db->_error_number ())
			log_message ( 'error', 'Activity_model.get_activities_by_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $query->result_array ();
	}
	public function get_activity_item_relation($activity_id, $global_item_id) {
		$this->db->where ( 'Activity_ID', $activity_id );
		$this->db->where ( 'Global_Item_ID', $global_item_id );
		$query = $this->db->get ( self::TABLE_ACTIVITY_ITEM );
		return $query->row_array ();
	}
	public function get_activity_item_relations($activity_id) {
		$this->db->where ( 'Activity_ID', $activity_id );
		$query = $this->db->get ( self::TABLE_ACTIVITY_ITEM );
		return $query->result_array ();
	}
	public function get_item_activity_relation($global_item_id) {
		$this->db->where ( 'Global_Item_ID', $global_item_id );
		$query = $this->db->get ( self::TABLE_ACTIVITY_ITEM );
		return $query->result_array ();
	}
	public function insert_activity_item_relation($activity_id, $global_item_id) {
		if (! $this->get_activity_item_relation ( $activity_id, $global_item_id )) {
			$result = $this->db->insert ( self::TABLE_ACTIVITY_ITEM, array (
					'Activity_ID' => $activity_id,
					'Global_Item_ID' => $global_item_id 
			) );
			if ($this->db->_error_number ())
				log_message ( 'error', 'Activity_model.insert_activity_item_relation: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return $result;
		}
		return TRUE;
	}
}
?>