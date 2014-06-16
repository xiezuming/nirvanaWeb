<?php
class Inv_recommendation_model extends CI_Model {
	public function query_recommended_info($input_data) {
		$cmd = FCPATH.'query_recommended_info.py';
		$result = shell_exec('python ' . $cmd . ' ' . escapeshellarg(json_encode($input_data)));
		$result = json_decode($result, true);
		if (!isset($result['title'])) {
			return NULL;
		} else {
			return $result;
		}
	}
	 
	public function query_inv_price($barcode, $title) {
		$data = array($barcode, $title);
		$cmd = FCPATH.'query_price.py';
		$result = shell_exec('python ' . $cmd . ' ' . escapeshellarg(json_encode($data)));
		$result = json_decode($result, true);
		if (!isset($result['price'])) {
			return NULL;
		} else {
			return $result;
		}
	}
}
?>
