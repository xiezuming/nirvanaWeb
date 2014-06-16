<br/>
<pre>
<?php 
$info = <<< xxx
Set WHERE clauses.
SQL:
SELECT * FROM (`inv_item`) 
	JOIN `inv_search_result` ON `inv_item`.`userId` = `inv_search_result`.`userId` and inv_item.itemId = inv_search_result.itemId 
	WHERE *************************
	ORDER BY `inv_item`.`userId` asc, `inv_item`.`itemId` asc 
	LIMIT 10;
xxx;
echo $info
?>
</pre>
<?php echo form_open('/inv2/') ?>
	<textarea name="where" rows="3" cols="50"><?php echo isset($where)?trim($where):''?></textarea><br/>
	<input type="submit" name="submit" value="Query"/>
<?php echo '</form>' ?>
<br/>

<?php echo 'Total:'.$count ?>
<table>
	<tr>
		<th>Id</th>
		<th>Title</th>
		<th>Barcode</th>
		<th>Photo</th>
	</tr>
	<?php foreach ($invs as $inv): ?>
	<tr>
		<td><?php echo anchor('/inv2/details/'.$inv['userId'].'/'.$inv['itemId'], $inv['userId'].'-'.$inv['itemId'])?></td>
		<td><?php echo $inv['title']?></td>
		<td><?php echo $inv['barcode']?></td>
		<td>
		<?php 
		if ($inv['photoname1']) {
			$url_orignal = site_url('/inv2/image_orignal/'.$inv['userId'].'/'.$inv['photoname1']);
			$url_thumbnail = site_url('/inv2/image_thumbnail/'.$inv['userId'].'/'.$inv['photoname1']);
			echo '<a href="'.$url_orignal.'" target="_blank"><img src="'.$url_thumbnail.'"/></a>';
		}
		?>
		</td>
	</tr>
	<?php endforeach ?>
</table>

