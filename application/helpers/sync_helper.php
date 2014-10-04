<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'create_wp_item' )) {
	function create_wp_item($global_item_id, $item_model, $meta_model) {
		$item = $item_model->get_item_by_global_id ( $global_item_id );
		if (! $item) {
			log_message ( 'error', 'create_wp_item: Can not find the item.' . $global_item_id );
			return FALSE;
		}
		
		// build data
		$first_image_row = $item_model->get_first_image ( $global_item_id );
		$item_photo_url = '';
		if ($first_image_row && strlen ( $first_image_row ['imageName'] ) > 4) {
			$item_photo_url = 'http://happitail.info/wetagimg/' . $item ['userId'] . '/' . $first_image_row ['imageName'];
			$postfix = $item ['availability'] == 'AB' ? '-360' : '-360sold';
			$item_photo_url = substr_replace ( $item_photo_url, $postfix, - 4, 0 );
		}
		$condition_row = $meta_model->get_meta_code ( 2, $item ['condition'] );
		$desc_prefix = $condition_row ? 'Condition: ' . $condition_row ['value'] . '.' : '';
		$category_row = $meta_model->get_meta_code ( 1, $item ['category'] );
		$catagory_id = $category_row ? $category_row ['pos'] : - 1;
		$catagory_name = $category_row ? $category_row ['value'] : '';
		$keyword = empty ( $item ['barcode'] ) ? $item ['title'] : $item ['barcode'];
		$amazon_link = 'http://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&tag=happitailcom-20&field-keywords=' . urlencode ( $keyword );
		$amazon_link = '<br/><a href="' . htmlspecialchars ( $amazon_link ) . '">View Similar items on Amazon</a>';
		$wp_item = array (
				'Item_ID' => $global_item_id,
				'Item_Name' => $item ['title'],
				'Item_Slug' => '',
				'Item_Description' => $desc_prefix . '<br/>' . str_replace ( "\n", '<br/>', $item ['desc'] ) . $amazon_link,
				'Item_Price' => '$' . $item ['expectedPrice'],
				'Item_Photo_URL' => $item_photo_url,
				'Category_ID' => $catagory_id,
				'Category_Name' => $catagory_name,
				'Item_Date_Created' => $item ['recCreateTime'],
				'Item_Display_Status' => 'Show' 
		);
		return $wp_item;
	}
}

if (! function_exists ( 'sync_wp_item' )) {
	function sync_wp_item($global_item_id, $user_id, $wp_item, $image_row_array, $wordpress_model) {
		$wordpress_model->db->trans_start ();
		
		// update WordPress item table
		if ($wordpress_model->get_item ( $global_item_id )) {
			$success = $wordpress_model->update_item ( $wp_item );
			if ($success)
				$success = $wordpress_model->delete_images ( $global_item_id );
		} else {
			$success = $wordpress_model->insert_item ( $wp_item );
		}
		if ($success) {
			// update WordPress item image table
			foreach ( $image_row_array as $image_row ) {
				$item_image_id = $image_row ['Global_Item_Image_ID'];
				$item_image_url = 'http://happitail.info/wetagimg/' . $user_id . '/' . $image_row ['imageName'];
				$item_image_url = substr_replace ( $item_image_url, '-800', - 4, 0 );
				$success = $wordpress_model->insert_image ( $item_image_id, $global_item_id, $item_image_url );
				if (! $success)
					break;
			}
		}
		
		$wordpress_model->db->trans_complete ();
		
		if ($wordpress_model->db->trans_status () === FALSE) {
			log_message ( 'error', 'sync_wp_item: Failed to update the database.' );
			return FALSE;
		} else {
			log_message ( 'debug', 'sync_wp_item: Synchronize to WordPress database successfully.' );
			return TRUE;
		}
	}
}

if (! function_exists ( 'resize_upload_images' )) {
	function resize_upload_images($global_item_id, $item_model) {
		$global_image_id_array = array ();
		$image_row_array = $item_model->get_images ( $global_item_id );
		foreach ( $image_row_array as $image_row ) {
			if ($image_row ['synchWp'] == 'N')
				array_push ( $global_image_id_array, $image_row ['Global_Item_Image_ID'] );
		}
		if (count ( $global_image_id_array ) > 0) {
			$cmd = FCPATH . 'scripts' . DIRECTORY_SEPARATOR . 'imageGenerator.py' . ' ' . escapeshellarg ( json_encode ( $global_image_id_array ) );
			$log_file = LOG_BASE_PATH . 'imageGenerator-' . date ( 'Y-m-d' ) . '.log';
			$cmd = $cmd . ' >> ' . $log_file . ' 2>>' . $log_file;
			log_message ( 'debug', $cmd );
			shell_exec ( 'python ' . $cmd );
		}
	}
}