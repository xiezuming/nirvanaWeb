
<h2>Please choose the most relevant category:</h2>

<table>
	<?php $first = true;?>
	<?php foreach ($categories as $category): ?>
	<tr>
		<td><input type='radio' id='<?php echo $category['catNum']?>'
			name='category' <?php echo $first?'checked':''?>><label
			for='<?php echo $category['catNum']?>'><?php echo $category['catNameLong']?>
		</label></td>
	</tr>
	<?php $first = false;?>
	<?php endforeach ?>
</table>
