<font color='red'>
<?php echo validation_errors(); ?>
</font>
<?php echo form_open('user/sign_up')?>
<table>
	<tr>
		<td>User Name</td>
	</tr>
	<tr>
		<td><?php echo form_input('userName', set_value('userName'), 'size="30" placeholder="someone@example.com"');?></td>
	</tr>
	<tr>
		<td>Name</td>
	</tr>
	<tr>
		<td><?php echo form_input('firstName', set_value('firstName'), 'size="30" placeholder="First"');?></td>
	</tr>
	<tr>
		<td><?php echo form_input('lastName', set_value('lastName'), 'size="30" placeholder="Last"');?></td>
	</tr>
	<tr>
		<td>Password</td>
	</tr>
	<tr>
		<td><?php echo form_password('password', '', 'size="30" placeholder="Create password"');?></td>
	</tr>
	<tr>
		<td><?php echo form_password('password_confirm', '', 'size="30" placeholder="Reenter password"');?></td>
	</tr>
	<tr>
		<td colspan='2'><input type="submit" value="Create" /></td>
	</tr>
</table>

<?php echo '</form>'?>


