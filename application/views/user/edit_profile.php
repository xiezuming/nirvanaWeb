<?php echo flash_message()?>
<script type="text/javascript" charset="utf-8">
	$("#flashmessage").animate({top: "0px"}, 1000 ).show('fast');
	$("#closemessage").click(
			function () {
				$(this).parent("div").fadeOut("slow");
			}
	);
</script>

<font color='red'>
<?php echo validation_errors(); ?>
</font>
<?php
$red_star = '<font color="red">*</font>';
$hidden = array (
		'userId' => $user ['userId'] 
);
?>

<?php echo form_open('user/edit_profile','', $hidden)?>
<div id='content'>
	<table>
		<tr>
			<td><label><?php echo $red_star?>Name:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('firstName', set_value('firstName', $user['firstName']), 'size="11" placeholder="First"');?>&nbsp;<?php echo form_input('lastName', set_value('lastName', $user['lastName']), 'id="lastName" size="11" placeholder="Last"');?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Alias:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('alias', set_value('alias', $user['alias']), 'id="alias" size="25" placeholder="First"');?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Email Address:</label></td>
		</tr>
		<tr>
			<td><input type='email' name='email'
				value='<?php echo set_value('email', $user['email'])?>' size='25'
				placeholder='someone@example.com' /></td>
		</tr>
		<tr>
			<td><label>Password:</label></td>
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
			<td><?php echo form_input('zipcode', set_value('zipcode',  $user['zipcode']), 'size="25"');?></td>
		</tr>
		<tr>
			<td><label>Phone Number:</label></td>
		</tr>
		<tr>
			<td><input type='tel' name='phoneNumber'
				value='<?php echo set_value('phoneNumber', $user['phoneNumber'])?>'
				size='25' /></td>
		</tr>
		<tr>
			<td><label>WeChat ID:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('wechatId', set_value('wechatId', $user['wechatId']), 'size="25"');?></td>
		</tr>
		<tr>
			<td><label>Group:</label></td>
		</tr>
		<?php foreach ($group_array as $group) {?>
		<tr>
			<td><?php echo '<label>' . form_checkbox('user_groups[]', $group['key'], set_checkbox('user_groups', $group['key'], in_array($group['key'], $user['user_groups']))) . $group['value'] . '</label>' ?></td>
		</tr>
		<?php }?>
		<tr>
			<td colspan='2' align='center'><input type="submit" value="Update" /></td>
		</tr>
	</table>
</div>
<?php echo '</form>'?>


