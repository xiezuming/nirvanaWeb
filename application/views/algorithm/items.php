
<h2>Please choose the most relevant category:</h2>

<table>
<?php echo form_open('algorithm/query_similar_itmes')?>
	<?php $first = true;?>
	<?php foreach ($items as $item): ?>
	<tr>
		<td>
		<?php
		echo form_radio ( array (
				'name' => 'catNum',
				'id' => $category ['catNum'],
				'value' => $category ['catNum'],
				'checked' => $first 
		) )?>
		<?php echo form_label($item['catNameLong'], $category['catNum'])?>
		</td>
	</tr>
	<?php $first = false;?>
	<?php endforeach ?>
	<tr>
		<td align='center'><?php echo form_submit('submit', 'OK')?></td>
	</tr>
<?php echo '</form>'?>

</table>
