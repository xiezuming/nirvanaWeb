<?php echo validation_errors('<div class="critical">', '</div>'); ?>

<h3>Update the Catalogue</h3>
<?php echo form_open('catalogue/update_catalogue', 'onsubmit="return confirm(\'Are you sure you want to insert/update?\');"')?>

<?php
define ( 'CELL_COUNT_PRE_ROW', 2 );

$editable_field_cells = array ();

foreach ( $field_names as $field_name ) {
	array_push ( $editable_field_cells, '<label class="label_text">' . $field_name . '</label>' );
	$input = '<input type="input" name="' . $field_name . '" size="45" />';
	array_push ( $editable_field_cells, $input );
}
array_push ( $editable_field_cells, '<label class="label_text">itemIds</label>' );
$input = '<textarea name="itemIds" cols="41" rows="5" ></textarea>';
array_push ( $editable_field_cells, $input );
?>

<table class="bordertable">
	<?php echo create_table_rows($editable_field_cells, CELL_COUNT_PRE_ROW)?>
</table>

<input type="submit" name="submit" value="Insert/Update Catalogue" />
<?php echo '</form>'?>

<hr />

<h3>Synchronize Catalogue to WordPress DB</h3>
<?php echo form_open('catalogue/test_synch_catalogue')?>

<label>global_catalogue_id</label>
<input name="global_catalogue_id" /><br/>
<input type="submit" value="synchronize" />

<?php echo '</form>'?>
