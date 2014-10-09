<?php
function mask_email($email, $mask_char = '*', $percent = 50) {
	list ( $user, $domain ) = preg_split ( "/@/", $email );
	
	$len = strlen ( $user );
	
	$mask_count = floor ( $len * $percent / 100 );
	
	$offset = floor ( ($len - $mask_count) / 2 );
	
	$masked = substr ( $user, 0, $offset ) . str_repeat ( $mask_char, $mask_count ) . substr ( $user, $mask_count + $offset );
	
	return ($masked . '@' . $domain);
}
?>
<h1 align='center'><?php echo $title?></h1>
<br />

<table>
	<tr>

	</tr>
	<tr>
		<th>Title</th>
		<th>Price</th>
		<th>Email</th>
		<th>Publish Time</th>
	</tr>
	<?php foreach ($wishlist_array as $wishlist): ?>
	<tr>
		<td><?php echo $wishlist['wishlist_text']?></td>
		<td>
			<?php
		$price_min = $wishlist ['price_min'] ? $wishlist ['price_min'] : 'N/A';
		$price_max = $wishlist ['price_max'] ? $wishlist ['price_max'] : 'N/A';
		echo $price_min . ' - ' . $price_max?>
		</td>
		<td><?php echo mask_email($wishlist['email'])?></td>
		<td><?php echo $wishlist['recUpdateTime']?></td>
	</tr>
	<?php endforeach ?>
</table>


