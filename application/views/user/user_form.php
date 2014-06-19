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

<p>Login</p>
<?php echo form_open('user/login')?>
<label>userName</label>
<input name="userName" />
<br />
<label>password</label>
<input name="password" type="password" />
<br />
<br />
<input type="submit" value="Login" />
<?php echo '</form>'?>
<hr />

<p>Logout</p>
<?php echo form_open('user/logout')?>
<label>userId</label>
<input name="userId" />
<br />
<input type="submit" value="Logout" />
<?php echo '</form>'?>
