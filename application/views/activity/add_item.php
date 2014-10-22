
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
	<?php
	for($i = 0; $i < 5; $i ++) {
		$display_style = ($i == 0) ? 'block' : 'none';
		?>	
	<tr>
		<td>
			<div id="image_file_div_<?php echo $i?>" style="display: <?php echo $display_style?>">
				<input type="file" id="image_file_<?php echo $i?>"
					name="image_file_<?php echo $i?>" size="40" />
			</div>
		</td>
	</tr>
	<?php
	}
	?>
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
		<td><label><?php echo $red_star?>Condition:</label></td>
	</tr>
	<tr>
		<td><?php echo form_dropdown('condition', $meta_condition, set_value('condition', 'GD'), 'style="width:270px"');?></td>
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
		<td><label><?php echo $red_star?>ZIP Code:</label></td>
	</tr>
	<tr>
		<td><?php echo form_input('zipcode', set_value('zipcode'), 'size="30"');?></td>
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

<script type="text/javascript">
<!--
for (var i=0; i<4; i++) {
	$(document).on('change','#image_file_' + i , function(){
		images_count = $('input[name*="image_file_names[]"]').length;
		input_name = $(this).attr("name");
		idx = parseInt(input_name.substr(input_name.length - 1));
		if (images_count + idx >= 4) return;
		next_div_id = "image_file_div_" + (idx+1);
		$( "#" + next_div_id).show( "slow" );
	});
}
//-->
</script>