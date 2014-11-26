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
		$message_text = $this->input->post ( 'message' );
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
				'message' => $message_text 
		);
		if ($this->message_model->add_message ( $message )) {
			// If the user used app, send the push notification, otherwise send a email.
			if ($to_user ['lastAppLoginTime']) {
				$this->_send_push_notification ( $from_user, $to_user, $item, $message_text );
			} else {
				$this->_send_email_notification ( $from_user, $to_user, $item, $message_text );
			}
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
		$where = array (
				'fromUserId' => $this->input->post ( 'fromUserId' ),
				'toUserId' => $this->input->post ( 'toUserId' ),
				'itemUuid' => $this->input->post ( 'itemUuid' ) 
		);
		if ($this->input->post ( 'recCreateTime' )) {
			$rec_create_time = $this->input->post ( 'recCreateTime' );
			$where ["recCreateTime <= FROM_UNIXTIME($rec_create_time)"] = NULL;
		}
		if ($this->message_model->mark_message_read ( $where )) {
			$data ['result'] = SUCCESS;
		} else {
			$data ['result'] = FAILURE;
			$data ['message'] = 'Internal Error: Failed to update the database.';
		}
		$this->output->set_content_type ( 'application/json' )->set_output ( json_encode ( $data ) );
	}
	/**
	 * Call Parser server API to send a push notification.
	 *
	 * @param array $from_user        	
	 * @param array $to_user        	
	 * @param array $item        	
	 * @param string $message_text        	
	 */
	private function _send_push_notification($from_user, $to_user, $item, $message_text) {
		$unread_message_count = $this->message_model->count_unread_messages ( $to_user ['userId'] );
		$this->load->helper ( 'parse_push' );
		$playload = array (
				"alert" => "{$from_user ['alias']}: $message_text",
				"badge" => $unread_message_count,
				"sound" => "alert.aiff",
				"t" => PUSH_TYPE_ALERT_MESSAGE,
				"i" => $item ['itemId'],
				"u" => $from_user ['userId'] 
		);
		send_notification ( $to_user ['userId'], $playload );
	}
	/**
	 * Call email sending API the send a new message notification.s
	 *
	 * @param array $from_user        	
	 * @param array $to_user        	
	 * @param array $item        	
	 * @param string $message_text        	
	 */
	private function _send_email_notification($from_user, $to_user, $item, $message_text) {
		$this->load->helper ( 'myemail' );
		$this->load->helper ( 'url' );
		$email_to = $to_user ['email'];
		$email_subject = "[Weee!] Notification";
		$data ['to_user'] = $to_user;
		$data ['from_user'] = $from_user;
		$data ['item'] = $item;
		$data ['message_text'] = $message_text;
		$email_body = $this->load->view ( 'message/email_template_new_message', $data, true );
		send_email ( '', $email_to, $email_subject, $email_body );
	}
}

?>
