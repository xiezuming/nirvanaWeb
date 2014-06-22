<h1>User Test Page</h1>
<hr />

<p>Create User</p>
<?php echo form_open('user/create_user')?>
<label>userName</label>
<input name="userName" />
<br />
<label>password</label>
<input name="password" type="password" />
<br />
<br />
<input type="submit" value="Create" />
<?php echo '</form>'?>
<hr />

<p>Sign In</p>
<?php echo form_open('user/sign_in')?>
<label>userName</label>
<input name="userName" />
<br />
<label>password</label>
<input name="password" type="password" />
<br />
<br />
<input type="submit" value="Sign In" />
<?php echo '</form>'?>
<hr />

