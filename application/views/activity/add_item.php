
<h1><?php echo $activity['Activity_Name']?></h1>

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
		'value' => set_value ( 'description' ),
		'rows' => '10',
		'cols' => '30' 
);
?>
<?php echo form_open_multipart('activity/add_item/'.$activity['Activity_ID']);?>

<table>
	<tr>
		<td><label><?php echo $red_star?>Title: (include Gender &amp; Size)</label></td>
	</tr>
	<tr>
		<td><?php echo form_input('title', set_value('title'), 'size="30"');?></td>
	</tr>
	<tr>
		<td><label><?php echo $red_star?>Picture:</label></td>
	</tr>
	<tr>
		<td><input type="file" name="image_file" size="40" /></td>
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
		<td><?php echo form_input('price', set_value('price'), 'size="30"');?></td>
	</tr>
	<tr>
		<td><label><?php echo $red_star?>Email:</label></td>
	</tr>
	<tr>
		<td><input type='email' name='email'
			value='<?php echo set_value('email')?>' size='30'
			placeholder='someone@example.com' /></td>
	</tr>
	<tr>
		<td><label>WeChat ID:</label></td>
	</tr>
	<tr>
		<td><?php echo form_input('wechatId', set_value('wechatId'), 'size="30"');?></td>
	</tr>
	<tr>
		<td><label>Please review the information carefully. <br />If evey this
				is correct, click Submit below
		</label></td>
	</tr>
	<tr>
		<td align="center"><input type="submit" value="Submit" /></td>
	</tr>
</table>

<?php echo '</form>'?>
