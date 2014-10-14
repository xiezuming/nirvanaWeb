<?php
class Report_model extends CI_Model {
	const TABLE_REPORT = 'item_report';
	public function get_events_where($where) {
		$this->db->order_by ( 'report_create_time', 'desc' );
		return $this->db->get_where ( self::TABLE_REPORT, $where )->result_array ();
	}
	public function get_report($report_id) {
		$this->db->where ( 'itemReportId', $report_id );
		return $this->db->get ( self::TABLE_REPORT )->row_array ();
	}
	public function add_report($data) {
		$this->db->insert ( self::TABLE_REPORT, array (
				'itemId' => $data ['itemId'],
				'reportUserId' => $data ['reportUserId'],
				'category' => $data ['category'],
				'description' => $data ['description'] 
		) );
		if ($this->db->_error_number ()) {
			log_message ( 'error', 'Report_model.add_report: ' . $this->db->_error_number () . ':' . $this->db->_error_message () );
			return FALSE;
		} else {
			return $this->db->insert_id ();
		}
	}
}
?>