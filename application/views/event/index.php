
<table>
	<tr>
		<th>Event</th>
		<td></td>
	</tr>
<?php
foreach ( $event as $key => $value ) {
	echo "<tr><th>$key</th><td>";
	if ($key == 'event_text') {
		$json_obj = json_decode ( $value );
		if ($json_obj) {
			$json_string = json_encode ( $json_obj, JSON_PRETTY_PRINT );
			if ($json_string)
				$value = $json_string;
		}
		echo '<textarea readonly style="width: 500px; height: 200px">';
		echo $value;
		echo "</textarea>";
	} else {
		echo $value;
		if ($key == 'event_finished' && $value == 'N') {
			echo '<br/>' . anchor ( "event/finish/{$event['event_id']}", 'Mask as Finished' );
		}
	}
	echo "</td></tr>";
}
?>


</table>

<hr />
<table>
	<tr>
		<th>User</th>
		<td></td>
	</tr>
	
<?php
foreach ( $user as $key => $value ) {
	echo "<tr><th>$key</th><td>$value</td></tr>";
}
?>
</table>