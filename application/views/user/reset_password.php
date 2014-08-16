<h2>Reset Password</h2>

<?php echo validation_errors('<div class="critical">', '</div>'); ?>

<?php
$hidden = array (
		'user_id' => $user_id,
		'reset_key' => $reset_key 
);
echo form_open ( 'user/reset_password', '', $hidden );
?>

<table>
	<tr>
		<td><label for="text">Choose a password</label></td>
		<td><input type="password" name="password"
			value="<?php echo set_value('password'); ?>" /></td>
	</tr>
	<tr>
		<td><label for="text">Repeat chosen password</label></td>
		<td><input type="password" name="password_confirm"
			value="<?php echo set_value('password_confirm'); ?>" /></td>
	</tr>
	<tr>
		<td colspan="2"><input type="submit" name="submit" value="Reset" /></td>
	</tr>
</table>

<?php echo '</form>'?>
