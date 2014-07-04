<html>
<head>
<title>Upload Form</title>
</head>
<body>

<?php echo $error;?>

<?php echo form_open_multipart('item/upload');?>

	<label>userId</label>
	<input name="userId" />
	<br />
	<input type="file" name="userfile" size="20" />
	<br />
	<br />
	<input type="submit" value="upload" />

<?php echo '</form>'?>

</body>
</html>