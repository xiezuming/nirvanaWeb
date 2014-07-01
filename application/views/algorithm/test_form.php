<h1>Algorithm Test Page</h1>
<hr />

<p>query_item_defaults_by_barcode</p>
<?php echo form_open('algorithm/query_item_defaults_by_barcode')?>
<label>barcode: </label>
<input name="barcode" size="30" />
<br />
<input type="submit" value="Query" />
<?php echo '</form>'?>
<hr />

<p>query_item_prices</p>
<?php echo form_open('algorithm/query_item_prices')?>
<table>
	<tr>
		<td><label>barcode: </label></td>
		<td><input name="barcode" size="30" /></td>
	</tr>
	<tr>
		<td><label>title:</label></td>
		<td><input name="title" size="30" /></td>
	</tr>
	<tr>
		<td><input type="submit" value="Query" /></td>
	</tr>
</table>
<?php echo '</form>'?>
<hr />

<p>query_categories_by_title</p>
<?php echo form_open('algorithm/query_categories_by_title')?>
<label>title: </label>
<input name="title" size="30" />
<br />
<input type="submit" value="Query" />
<?php echo '</form>'?>
<hr />

<p>query_categories_by_title</p>
<?php echo form_open('algorithm/query_similar_itmes')?>
<table>
	<tr>
		<td><label>category number: </label></td>
		<td><input name="catNum" size="30" /></td>
	</tr>
	<tr>
		<td><label>title:</label></td>
		<td><input name="title" size="30" /></td>
	</tr>
	<tr>
		<td><input type="submit" value="Query" /></td>
	</tr>
</table>
<?php echo '</form>'?>
<hr />

<p>query_item_defaults_by_similar_item</p>
<?php echo form_open('algorithm/query_item_defaults_by_similar_item')?>
<label>image url: </label>
<input name="itemUrl" size="30" />
<br />
<input type="submit" value="Query" />
<?php echo '</form>'?>
<hr />
