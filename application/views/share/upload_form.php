<html>
<meta http-equiv="content-type" content="text/html; charset=utf-8"
	lang="en-us">
<head>
<title>大小手亲子群 Cosutme Exchange</title>
</head>
<body>
	<h1>
		大小手亲子群 <br />Costume Exchange
	</h1>

	Please submit your costume information:

	<font color='red'>
	<?php echo $error;?>

	<?php echo validation_errors(); ?>
	</font>

<?php
$red_star = '<font color="red">*</font>';
$description_meta = array (
		'name' => 'description',
		'id' => 'description',
		'value' => set_value ( 'description' ),
		'rows' => '10',
		'cols' => '30' 
);
?>
<?php echo form_open_multipart('item/upload');?>

	<table>
		<tr>
			<td><label><?php echo $red_star?>Title: (include Gender &amp; Size)</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('title', set_value('title'), 'size="40"');?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Picture:</label></td>
		</tr>
		<tr>
			<td><input type="file" name="userfile" size="40" /></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Description: <br />(item condition
					and other notable things)</label></td>
		</tr>
		<tr>
			<td><?php echo form_textarea($description_meta)?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Price:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('price', set_value('price'), 'size="40"');?></td>
		</tr>
		<tr>
			<td><label><?php echo $red_star?>Email:</label></td>
		</tr>
		<tr>
			<td><input type='email' name='email'
				value='<?php echo set_value('email')?>' size='40'
				placeholder='someone@example.com' /></td>
		</tr>
		<tr>
			<td><label>WeChat ID:</label></td>
		</tr>
		<tr>
			<td><?php echo form_input('wechatId', set_value('wechatId'), 'size="40"');?></td>
		</tr>
		<tr>
			<td><label>Please review the information carefully. <br />If evey
					this is correct, click Submit below
			</label></td>
		</tr>
		<tr>
			<td><input type="submit" value="Submit"
				style="width: 100px; height: 50px;" /></td>
		</tr>
	</table>
	<hr />
	<br />If you want to edit an item you submitted,
	<br /> please contact
	<br /> WeChat: larry_weee
	<br /> Email: larry@wetagapp.com

<?php echo '</form>'?>

</body>
</html>