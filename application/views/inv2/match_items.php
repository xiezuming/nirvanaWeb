<table>
	<tr>
		<th></th>
		<th>Title</th>
		<th>Price</th>
		<th>Image</th>
	</tr>
	<?php
	if ($match_items && is_array($match_items)) {
		foreach ($match_items as $item): ?>
	<tr>
		<td><input type="button" value="Link" onclick='link("<?php echo $item['url']?>")'></td>
		<td><?php echo anchor($item['url'], $item['title'], 'target="_blank"')?></td>
		<td><?php echo $item['price']?></td>
		<td><img src="<?php echo $item['image']?>" height="200"></td>
	</tr>
	<?php 
		endforeach;
	} ?>
</table>
