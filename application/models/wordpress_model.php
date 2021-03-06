<?php
class Wordpress_model extends CI_Model {
	const TABLE_ITEM = 'wp_UPCP_Items';
	const TABLE_IMAGE = 'wp_UPCP_Item_Images';
	const TABLE_CATALOGUE = 'wp_UPCP_Catalogues';
	const TABLE_CATALOGUE_ITEM = 'wp_UPCP_Catalogue_Items';
	const TABLE_CATALOGUE_GROUP = 'wp_UPCP_Catalogue_Groups';
	const TABLE_ACTIVITY_ITEM = 'wp_UPCP_Activity_Items';
	/* ======== ITEM ======== */
	public function get_item($item_id) {
		$this->db->where ( 'Item_ID', $item_id );
		$query = $this->db->get ( self::TABLE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.get_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		$result = $query->row_array ();
		return $result;
	}
	public function insert_item($data) {
		$result = $this->db->insert ( self::TABLE_ITEM, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.insert_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function update_item($item) {
		$this->db->where ( 'Item_ID', $item ['Item_ID'] );
		$result = $this->db->update ( self::TABLE_ITEM, $item );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.update_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_item($item) {
		$this->db->where ( 'itemId', $item ['itemId'] );
		$this->db->delete ( self::TABLE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.delete_item: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
	}
	/* ======== IMAGE ======== */
	public function insert_image($item_image_id, $item_id, $item_image_url) {
		$result = $this->db->insert ( self::TABLE_IMAGE, array (
				'Item_Image_ID' => $item_image_id,
				'Item_ID' => $item_id,
				'Item_Image_URL' => $item_image_url 
		) );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.insert_image: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_images($item_id) {
		$this->db->where ( 'Item_ID', $item_id );
		$result = $this->db->delete ( self::TABLE_IMAGE );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.delete_images: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	/* ======== CATALOGUE ======== */
	public function get_catalogue($catalogue_id) {
		$this->db->where ( 'Catalogue_ID', $catalogue_id );
		$query = $this->db->get ( self::TABLE_CATALOGUE );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.get_catalogue: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		$result = $query->row_array ();
		return $result;
	}
	public function insert_catalogue($data) {
		$result = $this->db->insert ( self::TABLE_CATALOGUE, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.insert_catalogue: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function update_catalogue($data) {
		$this->db->where ( 'Catalogue_ID', $data ['Catalogue_ID'] );
		$result = $this->db->update ( self::TABLE_CATALOGUE, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.update_catalogue: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	/* ======== CATALOGUE ITEM ======== */
	public function insert_catalogue_item_relation($catalogue_item_id, $catalogue_id, $item_id, $position) {
		$result = $this->db->insert ( self::TABLE_CATALOGUE_ITEM, array (
				'Catalogue_Item_ID' => $catalogue_item_id,
				'Catalogue_ID' => $catalogue_id,
				'Item_ID' => $item_id,
				'Position' => $position 
		) );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.insert_catalogue_item_relation: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_catalogue_item_relation($catalogue_item_id) {
		$this->db->where ( 'Catalogue_Item_ID', $catalogue_item_id );
		$result = $this->db->delete ( self::TABLE_CATALOGUE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.delete_catalogue_item_relation: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_catalogue_all_relations($catalogue_id) {
		$this->db->where ( 'Catalogue_ID', $catalogue_id );
		$result = $this->db->delete ( self::TABLE_CATALOGUE_ITEM );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Wordpress_model.delete_catalogue_all_relations: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	/* ======== CATALOGUE GROUP ======== */
	public function fresh_group_catalogues($group_catalogues) {
		$this->db->trans_start ();
		
		$this->db->empty_table ( self::TABLE_CATALOGUE_GROUP );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'Wordpress_model.fresh_group_catalogues: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		}
		$this->db->insert_batch ( self::TABLE_CATALOGUE_GROUP, $group_catalogues );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'Wordpress_model.fresh_group_catalogues: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		}
		
		$this->db->trans_complete ();
		
		return $this->db->trans_status ();
	}
	/* ======== ACTIVITY ======== */
	public function get_item_relations($global_item_id) {
		$this->db->where ( 'Item_ID', $global_item_id );
		$query = $this->db->get ( self::TABLE_ACTIVITY_ITEM );
		return $query->result_array ();
	}
	public function get_activity_item_relation($activity_id, $global_item_id) {
		$this->db->where ( 'Activity_ID', $activity_id );
		$this->db->where ( 'Item_ID', $global_item_id );
		$query = $this->db->get ( self::TABLE_ACTIVITY_ITEM );
		return $query->row_array ();
	}
	public function insert_activity_item_relation($activity_id, $global_item_id) {
		if (! $this->get_activity_item_relation ( $activity_id, $global_item_id )) {
			$result = $this->db->insert ( self::TABLE_ACTIVITY_ITEM, array (
					'Activity_ID' => $activity_id,
					'Item_ID' => $global_item_id 
			) );
			if ($this->db->_error_number ())
				log_message ( 'error', 'Wordpress_model.insert_activity_item_relation: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return $result;
		}
		return TRUE;
	}
}
?>