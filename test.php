<!DOCTYPE head PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>

<head>
<script src="http://ajax.aspnetcdn.com/ajax/jQuery/jquery-1.11.1.min.js"></script>
<script type="text/javascript">
$(document).ready(function(){
	$("#b01").click(function(){
		$.post("index.php/event/contact_home", 
				{ 
					Action: "post", 
					name: "Xie Zuming",
					email: "xiezuming@hotmail.com",
					message: "test" },
				function (data, textStatus){
					if (data.result)
						$("#myDiv").html(data.message);
				}, "json");
  });
});
</script>
</head>

<body>

<div id="myDiv"><h2>Ha Ha</h2></div>
<button id="b01" type="button">Call</button>

</body>
</html>