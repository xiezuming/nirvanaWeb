<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

/**
 *
 * @property Message_model $message_model
 * @property User_model $user_model
 * @property Item_model $item_model
 */
class Message extends CI_Controller {
	function __construct() {
		parent::__construct ();
		$this->load->model ( 'message_model' );
		$this->load->model ( 'user_model' );
		$this->load->model ( 'item_model' );
	}
	
	/**
	 * Get the messages.
	 *
	 * @param string $user_id        	
	 */
	public function query_messages() {
		$user_id = $this->input->post ( 'userId' );
		$where = "(fromUserId = '$user_id' OR toUserId = '$user_id')";
		
		$rec_create_time = $this->input->post ( 'startTime' );
		if ($rec_create_time)
			$where .= " AND recCreateTime > FROM_UNIXTIME($rec_create_time) ";
		
		$limit = $this->input->post ( 'limit' ) ? $this->input->post ( 'limit' ) : null;
		$offset = $this->input->post ( 'offset' ) ? $this->input->post ( 'offset' ) : 0;
		
		$data ['result'] = SUCCESS;
		$data ['data'] = array (
				'messages' => $this->message_model->query_messages ( $where, $limit, $offset ) 
		);
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Add a message from the post data.
	 * POST: messageUuid, fromUserId, toUserId, itemUuid, message
	 */
	public function add_message() {
		$from_user_id = $this->input->post ( 'fromUserId' );
		$from_user = $this->user_model->get_user ( $from_user_id );
		$to_user_id = $this->input->post ( 'toUserId' );
		$to_user = $this->user_model->get_user ( $to_user_id );
		$item_uuid = $this->input->post ( 'itemUuid' );
		$item = $this->item_model->get_item ( $item_uuid );
		$image = $this->item_model->get_first_image ( $item ['Global_Item_ID'] );
		
		$message = array (
				'messageUuid' => $this->input->post ( 'messageUuid' ),
				'fromUserId' => $from_user_id,
				'fromUserName' => $from_user ['alias'],
				'toUserId' => $to_user_id,
				'toUserName' => $to_user ['alias'],
				'itemUuid' => $item_uuid,
				'itemUserId' => $item ['userId'],
				'itemTitle' => $item ['title'],
				'itemImageName' => $image ['imageName'],
				'message' => $this->input->post ( 'message' ) 
		);
		if ($this->message_model->add_message ( $message )) {
			// Send push notification
			$this->load->helper ( 'parse_push' );
			$notification_msg = "${from_user ['alias']} sent you a message.";
			send_notification ( $to_user_id, $notification_msg );
			
			$data ['result'] = SUCCESS;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Failed to update the database.';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	
	/**
	 * Mark the message as read.
	 * POST: messageUuid, fromUserId, toUserId, itemUuid
	 */
	public function mark_message_read() {
		if ($this->message_model->mark_message_read ( $this->input->post () )) {
			$data ['result'] = SUCCESS;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Failed to update the database.';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
}

?>