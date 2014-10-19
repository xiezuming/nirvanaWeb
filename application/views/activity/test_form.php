<?php echo validation_errors('<div class="critical">', '</div>'); ?>

<h3>Get Item b64UUID</h3>
<?php echo form_open('activity/get_item_b64UUID')?>

<label>itemId</label>
<input name="itemId" />
<br />
<label>Global_Item_ID</label>
<input name="global_item_id" />
<br />
<br />
<input type="submit" value="Get" />
<?php echo '</form>'?>



