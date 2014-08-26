<font color='red'>
<?php echo validation_errors(); ?>
</font>
<?php
$red_star = '<font color="red">*</font>';

$hidden = array (
		'user_id' => $user_id,
		'event_type' => 'contact' 
);

$message_data = array (
		'name' => 'event_text',
		'id' => 'event_text',
		'value' => set_value ( 'event_text' ),
		'rows' => '10',
		'cols' => '30' 
);

?>
<?php echo form_open('event/contact', '', $hidden)?>
<div id='content'>
	<table>
		<tr>
			<td><label>Subject<?php echo $red_star?></label></td>
		</tr>
		<tr>
			<td><?php echo form_input('event_sub_type', '', 'size="30" maxlength="45"')?></td>
		</tr>
		<tr>
			<td><label>Body<?php echo $red_star?></label></td>
		</tr>
		<tr>
			<td><?php echo form_textarea($message_data)?></td>
		</tr>
		<tr>
			<td align='center'><input type="submit" width="30" value="Send" /></td>
		</tr>
	</table>
</div>
<?php echo '</form>'?>


