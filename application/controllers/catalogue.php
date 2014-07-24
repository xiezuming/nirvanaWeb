<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;

/**
 *
 * @property Catalogue_model $catalogue_model
 * @property Item_model $item_model
 */
class Catalogue extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'catalogue_model' );
		$this->load->model ( 'item_model' );
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'catalogue/test_form', $data );
	}
	public function update_catalogue() {
		$input_data = $this->get_input_data ();
		$input_data ['synchWp'] = 'N';
		$catalgoue_id = $input_data ['catalogueId'];
		
		// retrieve the new relations from post
		$new_releation_itemIds = array ();
		$old_releation_itemIds = array ();
		$itemIdsString = $this->input->post ( 'itemIds' );
		if (! empty ( $itemIdsString )) {
			foreach ( explode ( ";", $itemIdsString ) as $itemId ) {
				$item = $this->item_model->get_item($itemId);
				if ($item) 
					array_push ( $new_releation_itemIds, $item['Global_Item_ID'] );
			}
		}
		log_message ( 'debug', 'update_catalogue: $new_releation_itemIds = ' . print_r ( $new_releation_itemIds, TRUE ) );
		
		$this->db->trans_start ();
		
		$catalgoue = $this->catalogue_model->get_catalogue ( $catalgoue_id );
		if ($catalgoue) {
			// fill $old_releation_itemIds
			$global_catalogue_id = $catalgoue['Global_Catalogue_ID'];
			$relations = $this->catalogue_model->get_catalogue_item_relations($global_catalogue_id);
			foreach ( $relations as $relation ) {
				array_push ( $old_releation_itemIds, $relation ['Global_Item_ID'] );	
			}

			$this->catalogue_model->update_catalogue ( $input_data );
		} else {
			// Insert mode
			$this->catalogue_model->insert_catalogue ( $input_data );
		}
		$catalgoue = $this->catalogue_model->get_catalogue ( $catalgoue_id );
		$global_catalogue_id = $catalgoue['Global_Catalogue_ID'];
		
		$insert_releation_itemIds = array_diff ( $new_releation_itemIds, $old_releation_itemIds );
		$delete_releation_itemIds = array_diff ( $old_releation_itemIds, $new_releation_itemIds );
		log_message ( 'debug', 'update_catalogue: $insert_releation_itemIds = ' . print_r ( $insert_releation_itemIds, TRUE ) );
		log_message ( 'debug', 'update_catalogue: $delete_releation_itemIds = ' . print_r ( $delete_releation_itemIds, TRUE ) );
		
		foreach ( $insert_releation_itemIds as $global_item_id ) {
			$this->catalogue_model->insert_catalogue_item_relation ( $global_catalogue_id, $global_item_id );
		}
		foreach ( $delete_releation_itemIds as $global_item_id ) {
			$this->catalogue_model->delete_catalogue_item_relation ( $global_catalogue_id, $global_item_id );
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
