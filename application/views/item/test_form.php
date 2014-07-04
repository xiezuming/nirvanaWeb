<?php echo validation_errors('<div class="critical">', '</div>'); ?>

<?php echo form_open('item/update_item', 'onsubmit="return confirm(\'Are you sure you want to insert/update?\');"')?>

<?php
define ( 'CELL_COUNT_PRE_ROW', 2 );

$editable_field_cells = array ();

foreach ( $field_names as $field_name ) {
	array_push ( $editable_field_cells, '<label class="label_text">' . $field_name . '</label>' );
	$input = '<input type="input" name="' . $field_name . '" size="45" />';
	array_push ( $editable_field_cells, $input );
}
array_push ( $editable_field_cells, '<label class="label_text">photoNames</label>' );
$input = '<input type="input" name="photoNames" size="45" />';
array_push ( $editable_field_cells, $input );
?>

<table class="bordertable">
	<?php echo create_table_rows($editable_field_cells, CELL_COUNT_PRE_ROW)?>
</table>

<input type="submit" name="submit" value="Insert/Update Item" />
<?php echo '</form>'?>

<hr />

<?php echo form_open_multipart('item/upload');?>

<label>userId</label>
<input name="userId" />
<br />
<input type="file" name="userfile" size="20" />
<br />
<br />
<input type="submit" value="upload" />

<?php echo '</form>'?>
