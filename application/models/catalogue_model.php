<?php
class Catalogue_model extends CI_Model {
	const TABLE_CATALOGUE = 'catalogue';
	const TABLE_CATALOGUE_ITEM = 'catalogue_item';
	public function get_catalogue($catalogueId) {
		$this->db->where ( 'catalogueId', $catalogueId );
		$query = $this->db->get ( self::TABLE_CATALOGUE );
		return $query->row_array ();
	}
	public function get_default_catalogue($userId) {
		$this->db->where ( 'userId', $userId );
		$this->db->where ( 'catalogueName', 'All Available Items' );
		$query = $this->db->get ( self::TABLE_CATALOGUE );
		$catalogue = $query->row_array ();
		if ($catalogue) {
			return $catalogue;
		} else {
			$catalogueId = $this->gen_uuid ();
			$data = array (
					'catalogueId' => $catalogueId,
					'catalogueName' => 'All Available Items',
					'userId' => $userId 
			);
			$this->db->insert ( self::TABLE_CATALOGUE, $data );
			return $this->get_catalogue ( $catalogueId );
		}
	}
	public function insert_catalogue($data) {
		$result = $this->db->insert ( self::TABLE_CATALOGUE, $data );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Catalogue_model.insert_catalogue: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function update_catalogue($catalogue) {
		$this->db->where ( 'catalogueId', $catalogue ['catalogueId'] );
		$result = $this->db->update ( self::TABLE_CATALOGUE, $catalogue );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Catalogue_model.insert_catalogue: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_catalogue($catalogue) {
		$this->db->where ( 'catalogueId', $catalogue ['catalogueId'] );
		$result = $this->db->delete ( self::TABLE_CATALOGUE );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Catalogue_model.insert_catalogue: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function insert_user_default_catalogue_item_relation($item) {
		$userId = $item ['userId'];
		$globalItemId = $item ['Global_Item_ID'];
		$catalogueName = 'All Available Items';
		
		// Get the user default catalogue. If not exist, create it.
		$this->db->where ( 'userId', $userId );
		$this->db->where ( 'catalogueName', $catalogueName );
		$query = $this->db->get ( self::TABLE_CATALOGUE );
		$catalogue = $query->row_array ();
		if (! $catalogue) {
			$catalogueId = $this->gen_uuid ();
			$currentTime = date ( 'Y-m-d H:i:s' );
			$data = array (
					'catalogueId' => $catalogueId,
					'catalogueName' => 'All Available Items',
					'userId' => $userId,
					'recCreateTime' => $currentTime,
					'recUpdateTime' => $currentTime,
					'synchWp' => 'N' 
			);
			if (! $this->insert_catalogue ( $data ))
				return FALSE;
			$catalogue = $this->get_catalogue ( $catalogueId );
		}
		$globalCatalogueId = $catalogue ['Global_Catalogue_ID'];
		
		if (! $this->get_catalogue_item_relation ( $globalCatalogueId, $globalItemId )) {
			return $this->insert_catalogue_item_relation ( $globalCatalogueId, $globalItemId );
		}
		return TRUE;
	}
	public function get_catalogue_item_relation($globalCatalogueId, $globalItemId) {
		$this->db->where ( 'Global_Catalogue_ID', $globalCatalogueId );
		$this->db->where ( 'Global_Item_ID', $globalItemId );
		$query = $this->db->get ( self::TABLE_CATALOGUE_ITEM );
		return $query->result_array ();
	}
	public function get_catalogue_item_relations($global_catalogue_id) {
		$this->db->where ( 'Global_Catalogue_ID', $global_catalogue_id );
		$this->db->order_by("Global_Item_ID", "desc");
		$query = $this->db->get ( self::TABLE_CATALOGUE_ITEM );
		return $query->result_array ();
	}
	public function insert_catalogue_item_relation($global_catalogue_id, $global_item_id) {
		$result = $this->db->insert ( self::TABLE_CATALOGUE_ITEM, array (
				'Global_Catalogue_ID' => $global_catalogue_id,
				'Global_Item_ID' => $global_item_id 
		) );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Catalogue_model.insert_catalogue_item_relation: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
		return $result;
	}
	public function delete_catalogue_item_relation($global_catalogue_id, $global_item_id) {
		$this->db->delete ( self::TABLE_CATALOGUE_ITEM, array (
				'Global_Catalogue_ID' => $global_catalogue_id,
				'Global_Item_ID' => $global_item_id 
		) );
		if ($this->db->_error_number ())
			log_message ( 'error', 'Catalogue_model.delete_catalogue_item_relation: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
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