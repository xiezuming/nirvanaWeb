
<h3>Item List</h3>
<table border="1" style="border-collapse: collapse">
	<tr>
		<th>Global_Item_ID</th>
		<th>user</th>
		<th>title</th>
		<th>price</th>
		<th>image</th>
		<th></th>
	</tr>
<?php
foreach ( $items as $item ) {
	$image_url = '/images/weee_app/' . $item ['userId'] . '/' . $item ['defaultImage'];
	?>
		<tr>
		<td><?php echo $item['Global_Item_ID']?></td>
		<td><?php echo $item['user']?></td>
		<td><?php echo $item['title']?></td>
		<td><?php echo $item['expectedPrice']?></td>
		<td><?php echo '<a href="'.$image_url.'" target="_blank"><img src="' . $image_url . '" height="100"/></a>' ?></td>
		<td><a
			href="<?php echo site_url('admin_item/view/'.$item['Global_Item_ID'])?>">More</a></td>
	</tr>

<?php
}
?>
		
</table>

