<?php
class Item_model extends CI_Model {
	const TABLE_ITEM = 'item';
	const TABLE_HISTORY = 'item_history';
	const TABLE_IMAGE = 'item_image';
	/* ======== ITEM ======== */
	public function get_item($itemId) {
		$this->db->where ( 'itemId', $itemId );
		$query = $this->db->get ( self::TABLE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Item_model.get_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		$result = $query->row_array ();
		return $result;
	}
	public function insert_item($data) {
		$result = $this->db->insert ( self::TABLE_ITEM, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Item_model.insert_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function update_item($item) {
		$this->db->where ( 'itemId', $item ['itemId'] );
		$result = $this->db->update ( self::TABLE_ITEM, $item );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Item_model.update_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_item($item) {
		$this->db->where ( 'itemId', $item ['itemId'] );
		$this->db->delete ( self::TABLE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Item_model.delete_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
	}
	/* ======== ITEM HISTORY ======== */
	public function insert_item_history($data) {
		$result = $this->db->insert ( self::TABLE_HISTORY, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Item_model.insert_item_history: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	/* ======== ITEM IMAGE ======== */
	public function get_images($globalItemId) {
		$this->db->where ( 'Global_Item_ID', $globalItemId );
		$query = $this->db->get ( self::TABLE_IMAGE );
		return $query->result_array ();
	}
	public function insert_image($globalItemId, $imageName) {
		$result = $this->db->insert ( self::TABLE_IMAGE, array (
				'Global_Item_ID' => $globalItemId,
				'imageName' => $imageName,
				'synchWp' => 'N' 
		) );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Item_model.insert_image: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_image($globalItemId, $imageName) {
		$this->db->where ( 'Global_Item_ID', $globalItemId );
		$this->db->where ( 'imageName', $imageName );
		$this->db->delete ( self::TABLE_IMAGE );
	}
}
?>