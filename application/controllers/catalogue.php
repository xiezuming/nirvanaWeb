<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

/**
 *
 * @property Catalogue_model $catalogue_model
 * @property Item_model $item_model
 * @property User_model $user_model
 */
class Catalogue extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'catalogue_model' );
		$this->load->model ( 'item_model' );
		$this->load->model ( 'user_model' );
	}
	public function test_page() {
		$this->load->helper ( 'form' );
		$this->load->library ( 'form_validation' );
		
		$data ['field_names'] = $this->get_field_names ();
		$this->load->view ( 'catalogue/test_form', $data );
	}
	public function get_catalogue_ids($userId) {
		$catalogue_id_array = array ();
		$catalogues_row = $this->catalogue_model->get_catalogues_by_user_id ( $userId );
		foreach ( $catalogues_row as $catalogue ) {
			array_push ( $catalogue_id_array, $catalogue ['catalogueId'] );
		}
		
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'catalogue_ids' => $catalogue_id_array 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function get_catalogue($catalogueId) {
		$catalogue = $this->catalogue_model->get_catalogue ( $catalogueId );
		if ($catalogue) {
			$item_ids = array ();
			$catalogue_items_row = $this->catalogue_model->get_catalogue_item_relations ( $catalogue ['Global_Catalogue_ID'] );
			foreach ( $catalogue_items_row as $catalogue_item ) {
				$item = $this->item_model->get_item_by_global_id ( $catalogue_item ['Global_Item_ID'] );
				array_push ( $item_ids, $item ['itemId'] );
			}
			$catalogue ['itemIds'] = implode ( ";", $item_ids );
			$catalogue ['recCreateTime'] = strtotime ( $catalogue ['recCreateTime'] );
			$catalogue ['recUpdateTime'] = strtotime ( $catalogue ['recUpdateTime'] );
			
			$data ['result'] = SUCCESS;
			$data ['data'] = array (
					'catalogue' => $catalogue 
			);
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Can not find the catalogue: ' . $catalogueId;
		}
		
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function update_catalogue() {
		$input_data = $this->get_input_data ();
		$input_data ['synchWp'] = 'N';
		$catalgoue_id = $input_data ['catalogueId'];
		$user_id = $input_data ['userId'];
		
		// the user only has one catalogu, set the url to his items home page
		$user = $this->user_model->get_user ( $user_id );
		if (! $user) {
			return output_json_result ( false, 'Internal Error: invalid user id' );
		}
		$input_data ['wpPostUrl'] = WEEE_WEB_BASE_URL . "/item/u/{$user['Global_User_ID']}";
		
		// retrieve the new relations from post
		$new_releation_itemIds = array ();
		$old_releation_itemIds = array ();
		$itemIdsString = $this->input->post ( 'itemIds' );
		if (! empty ( $itemIdsString )) {
			foreach ( explode ( ";", $itemIdsString ) as $itemId ) {
				$item = $this->item_model->get_item ( $itemId );
				if ($item)
					array_push ( $new_releation_itemIds, $item ['Global_Item_ID'] );
			}
		}
		log_message ( 'debug', 'update_catalogue: $new_releation_itemIds = ' . print_r ( $new_releation_itemIds, TRUE ) );
		
		$this->db->trans_start ();
		$catalgoue = $this->catalogue_model->get_catalogue ( $catalgoue_id );
		if ($catalgoue) {
			// fill $old_releation_itemIds
			$global_catalogue_id = $catalgoue ['Global_Catalogue_ID'];
			$relations = $this->catalogue_model->get_catalogue_item_relations ( $global_catalogue_id );
			foreach ( $relations as $relation ) {
				array_push ( $old_releation_itemIds, $relation ['Global_Item_ID'] );
			}
			$this->catalogue_model->update_catalogue ( $input_data );
		} else {
			// Insert mode
			$this->catalogue_model->insert_catalogue ( $input_data );
		}
		$catalgoue = $this->catalogue_model->get_catalogue ( $catalgoue_id );
		$global_catalogue_id = $catalgoue ['Global_Catalogue_ID'];
		
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
		
		if ($this->db->trans_status () === FALSE) {
			log_message ( 'error', 'Catalogue.update_catalogue: Failed to update the database.' );
			$data ['result'] = FAILURE;
			$data ['message'] = 'Failed to update the database.';
			$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
			return;
		}
		
		$data ['result'] = SUCCESS;
		$data ['data'] = $this->catalogue_model->get_catalogue_by_global_id ( $global_catalogue_id );
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function get_catalogue_post_url($catalogueId) {
		if (empty ( $catalogueId )) {
			echo 'ERROR: catalogueId is empty.';
			return;
		}
		$post_url = '';
		$catalogue = $this->catalogue_model->get_catalogue ( $catalogueId );
		if ($catalogue && ! empty ( $catalogue ['wpPostUrl'] )) {
			$post_url = $catalogue ['wpPostUrl'];
		}
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'post_url' => $post_url 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	private function get_field_names() {
		$field_names = array (
				"catalogueId" => "catalogueId",
				"catalogueName" => "catalogueName",
				"postContent" => "postContent",
				"userId" => "userId",
				"recCreateTime" => "recCreateTime",
				"recUpdateTime" => "recUpdateTime" 
		);
		return $field_names;
	}
	private function get_input_data() {
		log_message ( 'debug', 'input: ' . print_r ( $this->input->post (), TRUE ) );
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
