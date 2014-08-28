<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;

/**
 *
 * @property Catalogue_model $catalogue_model
 * @property Item_model $item_model
 * @property Wordpress_model $wordpress_model
 */
class Catalogue extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'catalogue_model' );
		$this->load->model ( 'item_model' );
		$this->load->model ( 'wordpress_model' );
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
		
		// synchronize to wp database
		$this->synch_catalogue ( $global_catalogue_id );
		
		// post the catalogue
		$this->post_catalogue ( $global_catalogue_id );
		
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
	public function sync_all_catalogues() {
		$catalogues = $this->catalogue_model->query_all_catalogues ( "synchWp = 'N' OR synchPost = 'N'" );
		$success_count = 0;
		$failure_count = 0;
		$failure_array = array ();
		foreach ( $catalogues as $catalogue ) {
			$global_catalogue_id = $catalogue ['Global_Catalogue_ID'];
			log_message ( 'debug', 'sync_all_catalogues: ' . $global_catalogue_id . '...' );
			
			$success_db = TRUE;
			$success_post = TRUE;
			if ($catalogue ['synchWp'] == 'N')
				$success_db = $this->synch_catalogue ( $global_catalogue_id );
			if ($catalogue ['synchWp'] == 'N')
				$success_post = $this->post_catalogue ( $global_catalogue_id );
			
			if ($success_db && $success_post) {
				$failure_count ++;
				array_push ( $failure_array, $global_catalogue_id );
			} else {
				$failure_count ++;
				array_push ( $failure_array, $global_catalogue_id );
			}
		}
		
		$data ['success_count'] = $success_count;
		$data ['failure_count'] = $failure_count;
		$data ['failure_array'] = $failure_array;
		$data ['result'] = $failure_count ? FAILURE : SUCCESS;
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	public function test_synch_catalogue() {
		$global_catalogue_id = $this->input->post ( 'global_catalogue_id' );
		if (empty ( $global_catalogue_id )) {
			echo 'ERROR: global_catalogue_id is empty.';
			return;
		}
		echo 'Restult: ' . var_export ( $this->synch_catalogue ( $global_catalogue_id ), TRUE );
	}
	/**
	 * Synchronize the catalogue and its relations information to WordPress database
	 *
	 * @param $global_catalogue_id: Global_Catalogue_ID        	
	 * @return boolean Returns TRUE if success.
	 */
	private function synch_catalogue($global_catalogue_id) {
		log_message ( 'debug', 'Start to synchronize the catalogue to WordPress DB.' );
		
		$catalogue = $this->catalogue_model->get_catalogue_by_global_id ( $global_catalogue_id );
		if (! $catalogue) {
			log_message ( 'error', 'Catalogue.synch_catalogue: Can not find the catalogue.' . $global_catalogue_id );
			return FALSE;
		}
		
		// build data
		$wp_catalogue_data = array (
				'Catalogue_ID' => $global_catalogue_id,
				'Catalogue_Name' => $catalogue ['catalogueName'],
				'Catalogue_Description' => '',
				'Catalogue_Layout_Format' => '',
				'Catalogue_Custom_CSS' => '',
				'Catalogue_Date_Created' => $catalogue ['recCreateTime'] 
		);
		$newRelationArray = $this->catalogue_model->get_catalogue_item_relations ( $global_catalogue_id );
		
		$wp_db = $this->load->database ( 'wp', TRUE );
		if (! $wp_db->initialize ()) {
			log_message ( 'error', 'Catalogue.synch_catalogue: Failed to connect the database.' );
			return FALSE;
		}
		
		$this->wordpress_model->db = $wp_db;
		$wp_db->trans_start ();
		
		// update WordPress catalgoue table
		if ($this->wordpress_model->get_catalogue ( $global_catalogue_id )) {
			$success = $this->wordpress_model->update_catalogue ( $wp_catalogue_data );
			if ($success)
				$success = $this->wordpress_model->delete_catalogue_all_relations ( $global_catalogue_id );
		} else {
			$success = $this->wordpress_model->insert_catalogue ( $wp_catalogue_data );
		}
		if ($success) {
			// update WordPress catalogue item relation table
			// TODO current sort the item order by their global itme id. Need think about it.
			$position = 0;
			foreach ( $newRelationArray as $newRelation ) {
				$success = $this->wordpress_model->delete_catalogue_item_relation ( $newRelation ['Global_Catalogue_Item_ID'] );
				if (! $success)
					break;
				$success = $this->wordpress_model->insert_catalogue_item_relation ( $newRelation ['Global_Catalogue_Item_ID'], $newRelation ['Global_Catalogue_ID'], $newRelation ['Global_Item_ID'], $position );
				if (! $success)
					break;
				$position ++;
			}
		}
		
		$wp_db->trans_complete ();
		
		if ($wp_db->trans_status () === FALSE) {
			log_message ( 'error', 'Catalogue.synch_catalogue: Failed to update the WordPresss database.' );
			return FALSE;
		} else {
			log_message ( 'debug', 'Catalogue.synch_catalogue: Synchronize to WordPress database successfully.' );
			$this->catalogue_model->update_catalogue ( array (
					'catalogueId' => $catalogue ['catalogueId'],
					'synchWp' => 'Y' 
			) );
			return TRUE;
		}
	}
	public function get_wp_posts() {
		$this->load->library ( 'xmlrpc' );
		$this->xmlrpc->server ( $this->config->config ['wp_rpc'] ['url'] );
		
		$this->xmlrpc->method ( 'wp.getPosts' );
		$this->xmlrpc->request ( array (
				0, // blog_id
				$this->config->config ['wp_rpc'] ['user'],
				$this->config->config ['wp_rpc'] ['password'] 
		) );
		print_r ( $this->xmlrpc_send_request ( $this->xmlrpc ) );
	}
	public function test_post_catalogue() {
		$global_catalogue_id = $this->input->post ( 'global_catalogue_id' );
		if (empty ( $global_catalogue_id )) {
			echo 'ERROR: global_catalogue_id is empty.';
			return;
		}
		echo 'Restult: ' . var_export ( $this->post_catalogue ( $global_catalogue_id ), TRUE );
	}
	private function post_catalogue($global_catalogue_id) {
		log_message ( 'debug', 'Start to post the catalogue to WordPress.' );
		
		$catalogue = $this->catalogue_model->get_catalogue_by_global_id ( $global_catalogue_id );
		if (! $catalogue) {
			log_message ( 'error', 'Catalogue.post_catalogue: Can not find the catalogue.' . $global_catalogue_id );
			return FALSE;
		}
		
		$this->load->library ( 'xmlrpc' );
		$this->xmlrpc->server ( $this->config->config ['wp_rpc'] ['url'] );
		
		$title = $catalogue ['catalogueName'];
		$post_content = $catalogue ['postContent'] . "[product-catalogue id='" . $global_catalogue_id . "']";
		
		if ($catalogue ['wpPostId']) {
			$response = $this->edit_post ( $this->xmlrpc, $catalogue ['wpPostId'], $title, $post_content );
		} else {
			$response = $this->new_post ( $this->xmlrpc, $title, $post_content );
			if ($response) {
				$catalogue ['wpPostId'] = $response;
				$post_info = $this->get_post ( $this->xmlrpc, $catalogue ['wpPostId'] );
				if ($post_info)
					$catalogue ['wpPostUrl'] = $post_info ['link'];
				else
					$catalogue ['wpPostUrl'] = 'http://happitail.info/catalog/?p=' . $catalogue ['wpPostId'];
			}
		}
		if ($response) {
			$catalogue ['synchPost'] = 'Y';
			if ($this->catalogue_model->update_catalogue ( $catalogue ))
				return TRUE;
			else {
				log_message ( 'error', 'catalogue.post_catalogue: Falied to update the catalogue table.' );
				return FALSE;
			}
		}
		return FALSE;
	}
	/**
	 * Create a post.
	 *
	 * @param CI_Xmlrpc $client        	
	 * @param string $title        	
	 * @param string $post_content        	
	 * @return integer post_id if OK, otherwise FALSE.
	 */
	private function new_post($client, $title, $post_content) {
		$client->method ( 'wp.newPost' );
		log_message ( 'debug', $client->method . ': ' . $title );
		$client->request ( array (
				0, // blog_id
				$this->config->config ['wp_rpc'] ['user'],
				$this->config->config ['wp_rpc'] ['password'],
				array (
						array (
								'post_title' => $title,
								'post_content' => $post_content,
								'post_status' => 'publish',
								'post_type' => 'post' 
						),
						'struct' 
				) 
		) );
		return $this->xmlrpc_send_request ( $client );
	}
	/**
	 * Edit the post.
	 *
	 * @param CI_Xmlrpc $client        	
	 * @param inetger $post_id        	
	 * @param string $title        	
	 * @param string $post_content        	
	 * @return bool True if OK, otherwise FALSE.
	 */
	private function edit_post($client, $post_id, $title, $post_content) {
		$client->method ( 'wp.editPost' );
		log_message ( 'debug', $client->method . ': ' . $post_id );
		$client->request ( array (
				0, // blog_id
				$this->config->config ['wp_rpc'] ['user'],
				$this->config->config ['wp_rpc'] ['password'],
				$post_id,
				array (
						array (
								'post_title' => $title,
								'post_content' => $post_content 
						),
						'struct' 
				) 
		) );
		return $this->xmlrpc_send_request ( $client );
	}
	/**
	 * Get the post
	 *
	 * @param CI_Xmlrpc $client        	
	 * @param integer $post_id        	
	 * @return The array of post information if OK, otherwise False.
	 */
	private function get_post($client, $post_id) {
		$client->method ( 'wp.getPost' );
		log_message ( 'debug', $client->method . ': ' . $post_id );
		$client->request ( array (
				0, // blog_id
				$this->config->config ['wp_rpc'] ['user'],
				$this->config->config ['wp_rpc'] ['password'],
				$post_id 
		) );
		return $this->xmlrpc_send_request ( $client );
	}
	private function xmlrpc_send_request($client) {
		if ($client->send_request ()) {
			$response = $client->display_response ();
			log_message ( 'debug', $client->method . ': response = ' . print_r ( $response, TRUE ) );
			return $response;
		} else {
			log_message ( 'error', $client->method . ': ' . $client->display_error () );
			return FALSE;
		}
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
