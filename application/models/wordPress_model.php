<?php
class WordPress_model extends CI_Model {
	const TABLE_ITEM = 'wp_UPCP_Items';
	const TABLE_IMAGE = 'wp_UPCP_Item_Images';
	/* ======== ITEM ======== */
	public function get_item($item_id) {
		$this->db->where ( 'Item_ID', $item_id );
		$query = $this->db->get ( self::TABLE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'WordPress_model.get_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		$result = $query->row_array ();
		return $result;
	}
	public function insert_item($data) {
		$result = $this->db->insert ( self::TABLE_ITEM, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'WordPress_model.insert_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function update_item($item) {
		$this->db->where ( 'Item_ID', $item ['Item_ID'] );
		$result = $this->db->update ( self::TABLE_ITEM, $item );
		if ($this->db->_error_number ())
			log_message ( 'error', 'WordPress_model.update_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_item($item) {
		$this->db->where ( 'itemId', $item ['itemId'] );
		$this->db->delete ( self::TABLE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'WordPress_model.delete_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
	}
	/* ======== IMAGE ======== */
	public function get_images($globalItemId) {
		$this->db->where ( 'Global_Item_ID', $globalItemId );
		$query = $this->db->get ( self::TABLE_IMAGE );
		return $query->result_array ();
	}
	public function insert_image($item_image_id, $item_id, $item_image_url) {
		$result = $this->db->insert ( self::TABLE_IMAGE, array (
				'Item_Image_ID' => $item_image_id,
				'Item_ID' => $item_id,
				'Item_Image_URL' => $item_image_url 
		) );
		if ($this->db->_error_number ())
			log_message ( 'error', 'WordPress_model.insert_image: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_images($item_id) {
		$this->db->where ( 'Item_ID', $item_id );
		$result = $this->db->delete ( self::TABLE_IMAGE );
		if ($this->db->_error_number ())
			log_message ( 'error', 'WordPress_model.delete_images: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
}
?>