
<h2>Please choose the most relevant category:</h2>

<table>
<?php echo form_open('algorithm/query_similar_itmes')?>
	<?php echo form_hidden('title', $query_title)?>
	<?php echo form_hidden('algo_session_id', $algo_session_id)?>
	
	<?php $first = true;?>
	<?php foreach ($categories as $category): ?>
	<tr>
		<td>
		<?php
		echo form_radio ( array (
				'name' => 'catNum',
				'id' => $category ['catNum'],
				'value' => $category ['catNum'],
				'checked' => $first 
		) )?>
		<?php echo form_label($category['catNameLong'], $category['catNum'])?>
		</td>
	</tr>
	<?php $first = false;?>
	<?php endforeach ?>
	<tr>
		<td align='center'><?php echo form_submit('submit', 'OK')?></td>
	</tr>
<?php echo '</form>'?>

</table>
