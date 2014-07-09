
<h2>Please choose an item similar to yours:</h2>

<?php echo form_open('algorithm/query_item_info_by_similar_item')?>
<?php echo form_hidden('title', $query_title)?>
<?php echo form_hidden('catNum', $catNum)?>
<table>
	<?php $i = 0;?>
	<?php foreach ($items as $item): ?>
	<tr>
	<?php
		$id = 'item' . $i;
		$radio_properties = array (
				'name' => 'similarItemUrl',
				'id' => $id,
				'value' => $item ['url'],
				'checked' => ! $i 
		);
		$image_properties = array (
				'src' => $item ['image'],
				'width' => '150' 
		);
		$i ++;
		?>
		
		<td><?php echo form_radio ( $radio_properties )?></td>
		<td><?php echo form_label ( img($image_properties), $id )?></td>
		<td><?php echo form_label($item['title'], $id)?></td>
	</tr>
	<?php endforeach ?>
	<tr>
		<td align='center' colspan='3'><?php echo form_submit('submit', 'OK')?></td>
	</tr>
</table>
<?php echo '</form>'?>


