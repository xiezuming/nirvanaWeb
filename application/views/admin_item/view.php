
<script type="text/javascript">
<!--
function copy_item() {

	if(confirm("Are you sure to copy the item to another user?"))
	{
		var target_user = $('select[name=user_list]').val();
		window.location.href = "<?php echo site_url('admin_item/copy/'.$item['Global_Item_ID'])?>/" + target_user;
// 	        alert("xxx");
	}
	else
	{
// 	        alert("yyy");
	}
}
//-->
</script>

<h3>Operations</h3>

Copy to: <?php echo form_dropdown('user_list', $user_select_list); ?>
<button onclick="copy_item()">Copy</button>

<hr />

<h3>User Details</h3>
<table border="1" style="border-collapse: collapse">
	<?php
	foreach ( $user as $key => $value ) {
		?>
	<tr>
		<th><?php echo $key?></th>
		<td><?php echo $value?></td>
	</tr>
	<?php
	}
	?>
</table>

<h3>Item Details</h3>
<table border="1" style="border-collapse: collapse">
	<?php
	foreach ( $item as $key => $value ) {
		?>
	<tr>
		<th><?php echo $key?></th>
		<td><?php echo $value?></td>
	</tr>
	<?php
	}
	?>
	<tr>
		<th></th>
		<td>
		<?php
		foreach ( $images as $image ) {
			$image_url = '/images/wetag_app/' . $item ['userId'] . '/' . $image ['imageName'];
			echo '<a href="' . $image_url . '" target="_blank"><img src="' . $image_url . '" height="150"/></a>';
		}
		?>
		</td>
	</tr>
</table>



