
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
		<td>
		<?php
		$div_id = 0;
		foreach ( $images as $image ) {
			$image_url = $image_url_base . $image ['imageName'];
			$image_url_small = str_replace ( '.jpg', '-360.jpg', $image_url );
			?>
			<div id="image_div_<?php echo $div_id?>">
				<input type="hidden" id="image_hidden_<?php echo $div_id?>"
					name="image_file_names[]" value="<?php echo $image ['imageName']?>">
				<a href="<?php echo $image_url?>" target="_blank"><img
					src="<?php echo $image_url_small?>" width="200"></a>
				<button type="button" onclick="hide_image_div(<?php echo $div_id?>)">Delete</button>
				<br />
			</div>
		<?php
			$div_id ++;
		}
		?>
		</td>
	</tr>
	<?php
	for($i = 0; $i < 5; $i ++) {
		$display_style = ($i == 0 && count ( $images ) < 5) ? 'block' : 'none';
		?>	
	<tr>
		<td>
			<div id="image_file_div_<?php echo $i?>" style="display: <?php echo $display_style?>">
				<input type="file" id="image_file_<?php echo $i?>" name="image_file_<?php echo $i?>" size="40" />
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
		<td><?php echo form_input('price', set_value('price', $item['expectedPrice']), 'size="30"');?></td>
	</tr>
	<tr>
		<td><label><?php echo $red_star?>Condition:</label></td>
	</tr>
	<tr>
		<td><?php echo form_dropdown('condition', $meta_condition, set_value('condition', $item['condition']), 'style="width:270px"');?></td>
	</tr>
	<tr>
		<td><label>Email: <?php echo $user['email']?></label></td>
	</tr>
	<tr>
		<td><label>WeChat ID: <?php echo $user['wechatId']?></label></td>
	</tr>
	<tr>
		<td><label>ZIP Code: <?php echo $user['zipcode']?></label></td>
	</tr>
	<tr>
		<td align="center"><input type="submit" value="Update" /></td>
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
function hide_image_div(image_div_id){
	$( "#image_hidden_" +  image_div_id).remove();
	$( "#image_div_" +  image_div_id).hide( "slow" );

	images_count = $('input[name*="image_file_names[]"]').length;
	idx = 3 - images_count;
	next_idx = idx + 1;
	if ( $('#image_file_' + idx).val() && $( "#image_file_div_" + next_idx).css('display') == 'none')
		$( "#image_file_div_" + next_idx).show( "slow" );
}
//-->
</script>
