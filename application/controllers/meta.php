<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );
const SUCCESS = 1;
const FAILURE = 0;
const UPLOAD_BASE_PATH = '/var/uploads/';

/**
 *
 * @property Meta_model $meta_model
 */
class Meta extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'meta_model' );
	}
	
	/**
	 * Echo the last update time of the meta data to the response.
	 * Output: The Unix timestamp.
	 * E.g.: {"result":1,"data":{"meta_type_last_update_time":1402940786}}
	 */
	public function get_meta_type_last_update_time() {
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'meta_type_last_update_time' => $this->meta_model->get_last_update_time () 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	
	/**
	 * Echo all meta types information to the response.
	 * Output: The array of meta type.
	 * E.g.: {"result":1,"data":{"meta_types":[{"typeId":"1","typeDesc":"Category","metaCodes":[{"key":"BOK","value":"Books"}]]}}
	 */
	public function get_meta_types() {
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'meta_types' => $this->meta_model->get_meta_types () 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
}

?>
