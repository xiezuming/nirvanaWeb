<h1>Algorithm Test Page</h1>
<hr />

<p>query_item_defaults_by_barcode</p>
<?php echo form_open('algorithm/query_item_defaults_by_barcode')?>
<label>barcode</label>
<input name="barcode" size="30"/>
<br />
<input type="submit" value="Query" />
<?php echo '</form>'?>
<hr />

<p>query_item_prices</p>
<?php echo form_open('algorithm/query_item_prices')?>
<label>barcode</label>
<input name="barcode" size="30"/>
<br />
<label>title</label>
<input name="title" size="30"/>
<br />
<input type="submit" value="Query" />
<?php echo '</form>'?>
<hr />

<p>query_categories_by_title</p>
<?php echo form_open('algorithm/query_categories_by_title')?>
<label>title</label>
<input name="title" size="30"/>
<br />
<input type="submit" value="Query" />
<?php echo '</form>'?>
<hr />

