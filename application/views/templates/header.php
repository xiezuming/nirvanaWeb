<html>
<head>
<meta http-equiv="content-type" content="text/html; charset=utf-8"
	lang="en-us">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title><?php echo $title ?> - Weee!</title>
<link rel="stylesheet"
	href="<?php echo base_url('/css/style_normal.css')?>">
<script type="text/javascript"
	src="<?php echo base_url('/js/jquery.js')?>"></script>
</head>

<body id="content">
	<h2>Weee!</h2>
	<hr />

	<?php echo '<div class="main">'?>
	
	<?php echo flash_message()?>
	<script type="text/javascript" charset="utf-8">
	$("#flashmessage").animate({top: "0px"}, 1000 ).show('fast');
	$("#closemessage").click(
			function () {
				$(this).parent("div").fadeOut("slow");
			}
	);
</script>