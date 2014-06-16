<?php
class Inv_meta_model extends CI_Model {
	const TABLE_TYPE = 'inv_meta_type';
	const TABLE_CODE = 'inv_meta_code';
	
	public function get_meta_code_item($typeId) {
		$where = array (
				'typeId' => $typeId 
		);
		$query = $this->db->get_where ( self::TABLE_CODE, $where );
		return $query->row_array ();
	}

	public function get_last_update_time() {
		$this->db->select_max('recUpdateTime');
		$query = $this->db->get( self::TABLE_TYPE );
		$time = $query->row_array()['recUpdateTime'];
		return strtotime($time);
	}
	
	public function add_inv_item($data) {
		return $this->db->insert ( self::TABLE_ITEM, $data );
	}
	public function delete_inv_itme($inv_item) {
		$where = array (
				'userId' => $inv_item ['userId'],
				'itemId' => $inv_item ['itemId'] 
		);
		$this->db->delete ( self::TABLE_ITEM, $where );
	}
	
	public function get_available_inv_list($where){
		$this->db->select('*');
		$this->db->from('inv_item');
		$this->db->join('inv_search_result', 'inv_item.userId = inv_search_result.userId and inv_item.itemId = inv_search_result.itemId');
		if (isset($where) && $where)
			$this->db->where($where, NULL, FALSE);
		$this->db->limit(10);
		$this->db->order_by("inv_item.userId asc, inv_item.itemId asc");
		$query = $this->db->get();
		return $query->result_array();
	}
	
	public function count_available_inv_list($where){
		$this->db->select('*');
		$this->db->from('inv_item');
		$this->db->join('inv_search_result', 'inv_item.userId = inv_search_result.userId and inv_item.itemId = inv_search_result.itemId');
		if (isset($where) && $where)
			$this->db->where($where, NULL, FALSE);
		return $this->db->count_all_results();
	}
}
?>