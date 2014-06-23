
<h2>Please choose the most relevant category:</h2>

<table>
	<?php foreach ($categories as $category): ?>
	<tr>
		<td><input type='radio' id='<?php echo $category['catNum']?>'
			name='category' checked><label for='<?php echo $category['catNum']?>'><?php echo $category['catNameLong']?>
		</label></td>
	</tr>

	<?php endforeach ?>
</table>
