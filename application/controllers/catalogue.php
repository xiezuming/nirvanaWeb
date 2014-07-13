<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;

/**
 *
 * @property Catalogue_model $catalogue_model
 */
class Catalogue extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'catalogue_model' );
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'catalogue/test_form', $data );
	}
	public function update_catalogue() {
		$input_data = $this->get_input_data ();
		$catalogueId = $input_data ['catalogueId'];
		
		log_message ( 'debug', 'update_catalogue: $catalogueId = ' . $catalogueId );
		
		$itemIdsString = $this->input->post ( 'itemIds' );
		$new_releation_itemIds = array ();
		if (! empty ( $itemIdsString )) {
			foreach ( explode ( ";", $itemIdsString ) as $itemId ) {
				array_push ( $new_releation_itemIds, $itemId );
			}
		}
		log_message ( 'debug', 'update_catalogue: $new_releation_itemIds = ' . print_r ( $new_releation_itemIds, TRUE ) );
		
		$insert_releation_itemIds = array ();
		$delete_releation_itemIds = array ();
		
		$catalgoue = $this->catalogue_model->get_catalogue ( $catalogueId );
		$this->db->trans_start ();
		if ($catalgoue) {
			// Update mode
			$this->catalogue_model->update_catalogue ( $input_data );
			
			$relations = $this->catalogue_model->get_catalogue_item_relations ( $catalogueId );
			foreach ( $relations as $relation ) {
				if (! in_array ( $relation ['itemId'], $new_releation_itemIds, TRUE ))
					array_push ( $delete_releation_itemIds, $relation ['itemId'] );
			}
			foreach ( $new_releation_itemIds as $newItemId ) {
				$found = FALSE;
				foreach ( $relations as $relation ) {
					if ($relation ['itemId'] === $newItemId) {
						$found = true;
						break;
					}
				}
				if (! $found)
					array_push ( $insert_releation_itemIds, $newItemId );
			}
		} else {
			// Insert mode
			$this->catalogue_model->insert_catalogue ( $input_data );
			
			foreach ( $new_releation_itemIds as $newItemId ) {
				array_push ( $insert_releation_itemIds, $newItemId );
			}
		}
		log_message ( 'debug', 'update_catalogue: $insert_releation_itemIds = ' . print_r ( $insert_releation_itemIds, TRUE ) );
		log_message ( 'debug', 'update_catalogue: $delete_releation_itemIds = ' . print_r ( $delete_releation_itemIds, TRUE ) );
		
		foreach ( $insert_releation_itemIds as $itemId ) {
			$this->catalogue_model->insert_catalogue_item_relation ( $catalogueId, $itemId );
		}
		foreach ( $delete_releation_itemIds as $itemId ) {
			$this->catalogue_model->delete_catalogue_item_relation ( $catalogueId, $itemId );
		}
		$this->db->trans_complete ();
		
		$data ['result'] = SUCCESS;
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	private function delete_file($file_path) {
		if (file_exists ( $file_path )) {
			unlink ( $file_path );
		}
	}
	private function get_field_names() {
		$field_names = array (
				"catalogueId" => "catalogueId",
				"catalogueName" => "catalogueName",
				"userId" => "userId",
				"recCreateTime" => "recCreateTime",
				"recUpdateTime" => "recUpdateTime" 
		);
		return $field_names;
	}
	private function get_input_data() {
		$input_data = array ();
		foreach ( $this->get_field_names () as $field_name ) {
			$field_value = $this->input->post ( $field_name );
			if (empty ( $field_value )) {
				$input_data [$field_name] = NULL;
			} else {
				// change
				if ($this->endsWith ( $field_name, 'Time' )) {
					$field_value = date ( 'Y-m-d H:i:s', $field_value );
				}
				$input_data [$field_name] = $field_value;
			}
		}
		return $input_data;
	}
	private function endsWith($haystack, $needle) {
		return $needle === "" || substr ( $haystack, - strlen ( $needle ) ) === $needle;
	}
}

?>
