<?php
class Catalogue_model extends CI_Model {
	const TABLE_CATALOGUE = 'catalogue';
	const TABLE_CATALOGUE_ITEM = 'catalogue_item';
	public function get_catalogue($catalogueId) {
		$this->db->where ( 'catalogueId', $catalogueId );
		$query = $this->db->get ( self::TABLE_CATALOGUE );
		return $query->row_array ();
	}
	public function insert_catalogue($data) {
		return $this->db->insert ( self::TABLE_CATALOGUE, $data );
	}
	public function update_catalogue($catalogue) {
		$this->db->where ( 'catalogueId', $catalogue ['catalogueId'] );
		return $this->db->update ( self::TABLE_CATALOGUE, $catalogue );
	}
	public function delete_catalogue($catalogue) {
		$this->db->where ( 'catalogueId', $catalogue ['catalogueId'] );
		$this->db->delete ( self::TABLE_CATALOGUE );
	}
	public function get_catalogue_item_relations($catalogueId) {
		$this->db->where ( 'catalogueId', $catalogueId );
		$query = $this->db->get ( self::TABLE_CATALOGUE_ITEM );
		return $query->result_array ();
	}
	public function insert_catalogue_item_relation($catalogueId, $itemId) {
		return $this->db->insert ( self::TABLE_CATALOGUE_ITEM, array (
				'catalogueId' => $catalogueId,
				'itemId' => $itemId 
		) );
	}
	public function delete_catalogue_item_relation($catalogueId, $itemId) {
		$this->db->delete ( self::TABLE_CATALOGUE_ITEM, array (
				'catalogueId' => $catalogueId,
				'itemId' => $itemId 
		) );
	}
}
?>