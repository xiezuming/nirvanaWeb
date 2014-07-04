<?php
class Item_model extends CI_Model {
	const TABLE_ITEM = 'item';
	const TABLE_HISTORY = 'item_history';
	const TABLE_PHOTO = 'item_photo';
	public function get_item($itemId) {
		$this->db->where ( 'itemId', $itemId );
		$query = $this->db->get ( self::TABLE_ITEM );
		return $query->row_array ();
	}
	public function insert_item($data) {
		return $this->db->insert ( self::TABLE_ITEM, $data );
	}
	public function update_item($item) {
		$this->db->where ( 'itemId', $item ['itemId'] );
		return $this->db->update ( self::TABLE_ITEM, $item );
	}
	public function delete_item($item) {
		$this->db->where ( 'itemId', $item ['itemId'] );
		$this->db->delete ( self::TABLE_ITEM );
	}
	public function get_available_inv_list($where) {
		$this->db->select ( '*' );
		$this->db->from ( 'inv_item' );
		$this->db->join ( 'inv_search_result', 'inv_item.userId = inv_search_result.userId and inv_item.itemId = inv_search_result.itemId' );
		if (isset ( $where ) && $where)
			$this->db->where ( $where, NULL, FALSE );
		$this->db->limit ( 10 );
		$this->db->order_by ( "inv_item.userId asc, inv_item.itemId asc" );
		$query = $this->db->get ();
		return $query->result_array ();
	}
	public function count_available_inv_list($where) {
		$this->db->select ( '*' );
		$this->db->from ( 'inv_item' );
		$this->db->join ( 'inv_search_result', 'inv_item.userId = inv_search_result.userId and inv_item.itemId = inv_search_result.itemId' );
		if (isset ( $where ) && $where)
			$this->db->where ( $where, NULL, FALSE );
		return $this->db->count_all_results ();
	}
	public function insert_item_history($data) {
		return $this->db->insert ( self::TABLE_HISTORY, $data );
	}
	public function get_photos($itemId) {
		$this->db->where ( 'itemId', $itemId );
		$query = $this->db->get ( self::TABLE_PHOTO );
		return $query->result_array ();
	}
	public function insert_photo($itemId, $photoName) {
		return $this->db->insert ( self::TABLE_PHOTO, array (
				'itemId' => $itemId,
				'photoName' => $photoName 
		) );
	}
	public function delete_photos($itemId) {
		$this->db->where ( 'itemId', $itemId );
		$this->db->delete ( self::TABLE_PHOTO );
	}
}
?>