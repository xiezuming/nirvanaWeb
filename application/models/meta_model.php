<?php
class Meta_model extends CI_Model {
	const TABLE_TYPE = 'meta_type';
	const TABLE_CODE = 'meta_code';
	public function get_meta_types() {
		$this->db->select ( 'typeId, typeDesc' );
		$this->db->order_by ( 'typeId', 'asc' );
		$query = $this->db->get_where ( self::TABLE_TYPE );
		$meta_types = $query->result_array ();
		$data = array ();
		foreach ( $meta_types as $meta_type ) {
			$type_id = $meta_type ['typeId'];
			$where = array (
					'typeId' => $type_id 
			);
			$this->db->select ( 'key, value' );
			$this->db->order_by ( 'pos', 'asc' );
			$meta_type ['metaCodes'] = $this->db->get_where ( self::TABLE_CODE, $where )->result_array ();
			$data [] = $meta_type;
		}
		return $data;
	}
	public function get_last_update_time() {
		$this->db->select_max ( 'recUpdateTime' );
		$query = $this->db->get ( self::TABLE_TYPE );
		$row = $query->row_array ();
		$time = $row ['recUpdateTime'];
		return strtotime ( $time );
	}
	public function get_meta_code($type_id, $code_key) {
		$where = array (
				'typeId' => $type_id,
				'key' => $code_key 
		);
		return $this->db->get_where ( self::TABLE_CODE, $where )->row_array ();
	}
	public function get_meta_codes($type_id) {
		$this->db->select ( 'key, value' );
		$this->db->order_by ( 'pos', 'asc' );
		return $this->db->get_where ( self::TABLE_CODE, array (
				'typeId' => $type_id 
		) )->result_array ();
	}
	public function get_meta_code_array($type_id) {
		$this->db->select ( 'key, value' );
		$this->db->order_by ( 'pos', 'asc' );
		$codes = $this->db->get_where ( self::TABLE_CODE, array (
				'typeId' => $type_id 
		) )->result_array ();
		$code_pairs = array ();
		foreach ( $codes as $code ) {
			$code_pairs [$code ['key']] = $code ['value'];
		}
		return $code_pairs;
	}
}
?>