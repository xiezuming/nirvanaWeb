<?php 
echo "Starting to connect MySQL...";
$connect=mysql_connect("127.0.0.1","root","root"); 
if(!$connect) 
	echo "Mysql Connect Error!"; 
else 
	echo "Mysql Connect Successfully!"; 
mysql_close(); 
?> 