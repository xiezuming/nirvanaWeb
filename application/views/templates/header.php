<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8"
	lang="en-us">
<title><?php echo $title ?> - Happitail Customer Service System</title>
<link rel="stylesheet" href="<?php echo base_url('/css/mystyle.css')?>">
<script type="text/javascript"
	src="<?php echo base_url('/js/jquery.js')?>"></script>
</head>

<body id="content">
	<table style="width: 100%">
		<tr>
			<td>
				<h3>InvHelper</h3>
			</td>
			<td align="right" valign="bottom"><?php echo welcome_left()?>
			</td>
		</tr>
	</table>
	<?php echo '<div class="main">'?>
	
	<?php echo flash_message() ?>
	<script type="text/javascript" charset="utf-8">
	$("#flashmessage").animate({top: "0px"}, 1000 ).show('fast');
	$("#closemessage").click(
			function () {
				$(this).parent("div").fadeOut("slow");
			}
	);
</script>