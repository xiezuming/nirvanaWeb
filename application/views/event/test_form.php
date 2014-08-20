<?php echo validation_errors('<div class="critical">', '</div>'); ?>

<h3>Insert the Event</h3>
<?php echo form_open('event/add_event', 'onsubmit="return confirm(\'Are you sure you want to insert?\');"')?>

<?php
define ( 'CELL_COUNT_PRE_ROW', 2 );

$editable_field_cells = array ();

foreach ( $field_names as $field_name ) {
	array_push ( $editable_field_cells, '<label class="label_text">' . $field_name . '</label>' );
	$input = '<input type="input" name="' . $field_name . '" size="45" />';
	array_push ( $editable_field_cells, $input );
}
?>

<table class="bordertable">
	<?php echo create_table_rows($editable_field_cells, CELL_COUNT_PRE_ROW)?>
</table>

<input type="submit" name="submit" value="Insert" />
<?php echo '</form>'?>

<hr />

<h3>Insert 'Sell to Wetag' Event</h3>
<?php echo form_open('event/add_sell_to_wetag_event', 'onsubmit="return confirm(\'Are you sure you want to insert?\');"')?>

<?php

$editable_field_cells = array ();
array_push ( $editable_field_cells, '<label class="label_text">user_id</label>' );
array_push ( $editable_field_cells, '<input type="input" name="user_id" size="45" />' );
array_push ( $editable_field_cells, '<label class="label_text">event_text</label>' );
array_push ( $editable_field_cells, '<input type="input" name="event_text" size="45" />' );
?>

<table class="bordertable">
	<?php echo create_table_rows($editable_field_cells, CELL_COUNT_PRE_ROW)?>
</table>

<input type="submit" name="submit" value="Insert" />
<?php echo '</form>'?>

<hr />
