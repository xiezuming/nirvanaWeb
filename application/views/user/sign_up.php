<font color='red'>
<?php echo validation_errors(); ?>
</font>
<?php
$red_star = '<font color="red">*</font>';
?>
<?php echo form_open('user/sign_up')?>
<div id='content'>
	<table>
		<tr>
			<td><label><?php echo $red_star?>Name:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('firstName', set_value('firstName'), 'size="11" placeholder="First"');?>&nbsp;<?php echo form_input('lastName', set_value('lastName'), 'id="lastName" size="11" placeholder="Last" onblur="fill_user_name()"');?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Email Address:</label></td>
		</tr>
		<tr>
			<td><input type='email' name='email'
				value='<?php echo set_value('email')?>' size='25'
				placeholder='someone@example.com' /></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Password:</label></td>
		</tr>
		<tr>
			<td><?php echo form_password('password', '', 'size="25" placeholder="Create password"');?></td>
		</tr>
		<tr>
			<td><?php echo form_password('password_confirm', '', 'size="25" placeholder="Reenter password"');?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>ZIP Code:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('zipcode', set_value('zipcode'), 'size="25"');?></td>
		</tr>
		<tr>
			<td><label>Phone Number:</label></td>
		</tr>
		<tr>
			<td><input type='tel' name='phoneNumber'
				value='<?php echo set_value('phoneNumber')?>' size='25' /></td>
		</tr>
		<tr>
			<td><label>WeChat ID:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('wechatId', set_value('wechatId'), 'size="25"');?></td>
		</tr>
		<tr>
			<td colspan='2' align='center'><input type="submit" value="Create" /></td>
		</tr>
	</table>
</div>
<?php echo '</form>'?>

<script type="text/javascript">
function fill_user_name(x)
{
	var alias = document.getElementById("alias").value;
	if (!alias) {
		document.getElementById("alias").value = document.getElementById("lastName").value;
	}
}
</script>

