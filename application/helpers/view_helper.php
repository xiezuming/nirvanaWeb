<?php
if (! defined ( 'BASEPATH' ))
	exit ( 'No direct script access allowed' );

if (! function_exists ( 'meta_code_array' )) {
	function meta_code_array($meta_type_name, $need_first_empty_item = true) {
		$CI = & get_instance ();
		$CI->load->model ( 'meta_model' );
		$arr = $CI->meta_model->get_meta_code_array_by_type ( $meta_type_name );
		if ($need_first_empty_item) {
			$arr = array_reverse ( $arr, true );
			$arr [''] = '';
			$arr = array_reverse ( $arr, true );
		}
		return $arr;
	}
}

if (! function_exists ( 'meta_code_desc' )) {
	function meta_code_desc($meta_type_name, $meta_code_key) {
		if (! isset ( $meta_code_key ) || trim ( $meta_code_key ) == '') {
			return '';
		}
		
		$CI = & get_instance ();
		$CI->load->model ( 'meta_model' );
		$value = $CI->meta_model->get_meta_code_desc ( $meta_type_name, $meta_code_key );
		if (! isset ( $value )) {
			$value = $meta_code_key . '(No Match)';
		}
		return $value;
	}
}

if (! function_exists ( 'create_field_input' )) {
	function create_field_input_tag(Table_field $table_field, $default = '', $hidden = FALSE) {
		$name = $table_field->get_name ();
		$value = set_value ( $table_field->get_name (), $default );
		
		if ($hidden) {
			return '<input type="hidden" name="' . $name . '" value="' . $value . '" />';
		}
		
		$view_style = $table_field->get_view_style ();
		if (strpos ( $view_style, 'input' ) === 0) {
			return '<input type="input" name="' . $name . '" value="' . $value . '" />';
		} else if (strpos ( $view_style, 'textarea' ) === 0) {
			$attribute = strlen ( $view_style ) > 8 ? substr ( $view_style, 8 ) : '';
			return '<textarea name="' . $name . '" ' . $attribute . ' >' . $value . '</textarea>';
		} else if (strpos ( $view_style, 'select' ) === 0) {
			if (strlen ( $view_style ) <= 7) {
				return '<input type="input" name="' . $name . '" value="' . $value . '" />';
			} else {
				$meta_type_name = trim ( substr ( $view_style, 7 ) );
				$options = meta_code_array ( $meta_type_name );
				$tag = form_dropdown ( $name, meta_code_array ( $meta_type_name ), $value );
				if (! array_key_exists ( $value, $options )) {
					$tag .= 'No Match(' . $value . ')';
				}
				return $tag;
			}
		} else {
			return '';
		}
	}
}

if (! function_exists ( 'create_field_view_tag' )) {
	function create_field_view_tag(Table_field $table_field, $value, $attr = '') {
		$view_style = $table_field->get_view_style ();
		
		if (strpos ( $view_style, 'input' ) === 0 || strpos ( $view_style, 'select' ) === 0) {
			if (strpos ( $view_style, 'select' ) === 0) {
				if (strlen ( $view_style ) > 7) {
					$meta_type_name = trim ( substr ( $view_style, 7 ) );
					$value = meta_code_desc ( $meta_type_name, $value );
				}
			}
			return '<label ' . $attr . '>' . $value . '</lable>';
		} else if (strpos ( $view_style, 'textarea' ) === 0) {
			$custom_attr = strlen ( $view_style ) > 8 ? substr ( $view_style, 8 ) : '';
			return '<textarea name="' . $table_field->get_name () . '" ' . $attr . ' ' . $custom_attr . ' readonly>' . $value . '</textarea>';
		} else {
			return '';
		}
	}
}

if (! function_exists ( 'create_table_rows' )) {
	function create_table_rows($cells, $cell_count_pre_row) {
		$ret_str = '';
		for($i = 0; $i < count ( $cells ); $i ++) {
			if ($i % $cell_count_pre_row == 0)
				$ret_str .= "<tr>\n";
			
			$ret_str .= '<td>' . $cells [$i] . "</td>\n";
			
			if ($i % $cell_count_pre_row == $cell_count_pre_row - 1)
				$ret_str .= "</tr>\n";
		}
		
		if (count ( $cells ) % $cell_count_pre_row != 0) {
			$ret_str .= "<td colspan=\"" . ($cell_count_pre_row - count ( $cells ) % $cell_count_pre_row) . "\"/></tr>\n";
		}
		return $ret_str;
	}
}

if (! function_exists ( 'create_key_value_table' )) {
	function create_key_value_table($val_array, $style = '') {
		$ret_str = "<table style='$style'>";
		foreach ( $val_array as $key => $value ) {
			$ret_str .= "<tr><th>$key</th><td>$value</td></tr>\n";
		}
		$ret_str .= '</table>';
		return $ret_str;
	}
}

if (! function_exists ( 'welcome_left' )) {
	function welcome_left() {
		$username = '';
		$CI = & get_instance ();
		if ($CI->session->userdata ( 'USER' )) {
			$user = $CI->session->userdata ( 'USER' );
			$username = $user ['username'];
		}
		
		return 'Welcome ' . $username . '!
				[' . anchor ( '/', 'Home' ) . ']
						[' . anchor ( '/home/logout/', 'Logout' ) . ']';
	}
}

if (! function_exists ( 'create_img_tag' )) {
	function create_img_tag($title, $img_name, $jump_uri = '', $href_attributes = '') {
		$img_tag = '<img class="imageicon" src=' . base_url ( '/img/' . $img_name . '.png' ) . ' title="' . $title . '"/>';
		if ($jump_uri == '') {
			return $img_tag;
		} else {
			return anchor ( $jump_uri, $img_tag, $href_attributes );
		}
	}
}

if (! function_exists ( 'flash_message' )) {
	function flash_message() {
		// get flash message from CI instance
		$ci = & get_instance ();
		$flashmsg = $ci->session->flashdata ( 'falshmsg' );
		$html = '';
		if (is_array ( $flashmsg )) {
			$html = '<div id="flashmessage" class="' . $flashmsg ['type'] . '">
					<img style="float: right; cursor: pointer" id="closemessage" src="' . base_url () . 'img/close.png" />
							<p>' . $flashmsg ['content'] . '</p>
									</div>';
		}
		return $html;
	}
}
