
	<h1>
		<?php echo $activity['Activity_Name']?>
	</h1>

	<?php echo $activity['Activity_Desc']?>
	<br />
	<br />

	<font color='red'>
	<?php echo $error;?>

	<?php echo validation_errors(); ?>
	</font>
	
<?php
$red_star = '<font color="red">*</font>';
$description_meta = array (
		'name' => 'description',
		'id' => 'description',
		'value' => set_value ( 'description', $item ['desc'] ),
		'rows' => '10',
		'cols' => '30' 
);
?>
<?php echo form_open_multipart('activity/edit_item/'.$b64_item_id);?>

	<table>
		<tr>
			<td><label><?php echo $red_star?>Title: (include Gender &amp; Size)</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('title', set_value('title', $item['title']), 'size="30"');?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Picture:</label></td>
		</tr>
		<tr>
			<td><input type="file" name="image_file" size="40" /></td>
		</tr>
		<tr>
			<td><a href="<?php echo $image_url?>" target="_blank"><img
					src="<?php echo str_replace('.jpg', '-360.jpg', $image_url)?>"
					width="200"></a></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Description: <br />(item condition
					and other notable things)</label></td>
		</tr>
		<tr>
			<td><?php echo form_textarea($description_meta)?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Price:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('price', set_value('price', $item['expectedPrice']), 'size="30"');?></td>
		</tr>
		<tr>
			<td><label>Email: <?php echo $user['email']?></label></td>
		</tr>
		<tr>
			<td><label>WeChat ID: <?php echo $user['wechatId']?></label></td>
		</tr>
		<tr>
			<td align="center"><input type="submit" value="Update"
				 /></td>
		</tr>
	</table>

<?php echo '</form>'?>
