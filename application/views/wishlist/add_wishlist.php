<h1 align='center'><?php echo $activity['Activity_Name']?></h1>
<h2 align='center'><?php echo $title?></h2>

<?php
$red_star = '<font color="red">*</font>';
?>
<?php echo form_open("wishlist/add_wishlist/" . $activity['Activity_ID']);?>

<table>
	<tr>
		<td><font color='red'>
	<?php echo $error;?>
		</font></td>
	</tr>
	<tr>
		<td><label><?php echo $red_star?>Title</label>
			<?php echo form_error('wishlist_text'); ?>
		</td>
	</tr>
	<tr>
		<td><?php echo form_input('wishlist_text', set_value('wishlist_text'), 'style="width: 275" placeholder="For example: coffee maker"');?></td>
	</tr>
	<tr>
		<td><label>Price:</label>
			<?php echo form_error('price_min'); ?>
			<?php echo form_error('price_max'); ?>
		</td>
	</tr>
	<tr>
		<td><input type='number' name='price_min'
			value='<?php echo set_value('price_min')?>' style='width: 130' /> - <input
			type='number' name='price_max'
			value='<?php echo set_value('price_max')?>' style='width: 130' /></td>
	</tr>
	<tr>
		<td><label><?php echo $red_star?>Email:</label>
			<?php echo form_error('email'); ?>
		</td>
	</tr>
	<tr>
		<td><input type='email' name='email'
			value='<?php echo set_value('email')?>' style="width: 275"
			placeholder='someone@example.com' /></td>
	</tr>
	<tr>
		<td><label>WeChat ID:</label></td>
	</tr>
	<tr>
		<td><?php echo form_input('wechatId', set_value('wechatId'), 'style="width: 275"');?></td>
	</tr>
	<tr>
		<td><label>ZIP Code:</label></td>
	</tr>
	<tr>
		<td><?php echo form_input('zipcode', set_value('zipcode'), 'style="width: 275"');?></td>
	</tr>
	<tr>
		<td><label>Please review the information carefully. <br />If evey this
				is correct, click Submit below
		</label></td>
	</tr>
	<tr>
		<td align="center"><input type="submit" value="Submit" /></td>
	</tr>
</table>

<?php echo '</form>'?>

<script type="text/javascript">
<!--

//-->
</script>