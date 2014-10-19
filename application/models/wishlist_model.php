<?php
class Wishlist_model extends CI_Model {
	const TABLE_WISHLIST = 'wishlist';
	public function query_published_wishlist($activiy_id) {
		$this->db->from ( self::TABLE_WISHLIST );
		$this->db->where ( "activity_id = $activiy_id AND published = 'Y' AND recUpdateTime >= DATE_SUB(NOW(), INTERVAL 14 DAY)" );
		$this->db->order_by ( "recUpdateTime", "desc" );
		$query = $this->db->get ();
		$result = $query->result_array ();
		return $result;
	}
	public function query_wishlist_by_uuid($wishlist_uuid) {
		$where = array (
				'wishlist_uuid' => $wishlist_uuid 
		);
		$query = $this->db->get_where ( self::TABLE_WISHLIST, $where );
		$wishlist = $query->row_array ();
		return $wishlist;
	}
	public function add_wishlist($data) {
		$this->db->insert ( self::TABLE_WISHLIST, $data );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'Wishlist_model.add_wishlist: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		}
		return TRUE;
	}
	public function update_wishlist($wishlist_uuid, $data) {
		$this->db->where ( 'wishlist_uuid', $wishlist_uuid );
		$result = $this->db->update ( self::TABLE_WISHLIST, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wishlist_model.update_wishlist: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
}
?>