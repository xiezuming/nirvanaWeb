<h1>User Test Page</h1>
<hr />

<p><?php echo anchor('user/sign_up', 'Sign Up')?></p>
<hr />

<p>Sign In</p>
<?php echo form_open('user/sign_in')?>
<label>email</label>
<input name="email" />
<br />
<label>password</label>
<input name="password" type="password" />
<br />
<br />
<input type="submit" value="Sign In" />
<?php echo '</form>'?>
<hr />

<p>Sign In with Facebook id</p>
<?php echo form_open('user/sign_in_fb')?>
<label>fbUserId</label>
<input name="fbUserId" />
<br />
<label>firstName</label>
<input name="firstName" />
<br />
<label>lastName</label>
<input name="lastName" />
<br />
<label>alias</label>
<input name="alias" />
<br />
<label>email</label>
<input name="email" />
<br />
<br />
<input type="submit" value="Sign In" />
<?php echo '</form>'?>
<hr />

<p>Update Wish List</p>
<?php echo form_open('user/update_wish_list')?>
<label>userId</label>
<input name="userId" />
<br />
<label>wishList</label>
<input name="wishList" />
<br />
<input type="submit" value="Update" />
<?php echo '</form>'?>
<hr />

<p>Send Reset Password Mail</p>
<?php echo form_open('user/reset_password_mail')?>
<label>email_address</label>
<input name="email_address" />
<br />
<input type="submit" value="Send" />
<?php echo '</form>'?>
<hr />
