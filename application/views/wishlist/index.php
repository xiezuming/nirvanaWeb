<h1 align='center'><?php echo $activity['Activity_Name']?></h1>
<h2 align='center'><?php echo $title?></h2>

<table id='wishlist_table'>
	<tr>
		<td colspan='4'><?php echo anchor('wishlist/add_wishlist/'.$activity['Activity_ID'], 'Submit Your Wish List')?></td>
	</tr>
	<tr>
		<th>Title</th>
		<th>Price</th>
		<th>Publish Date</th>
		<th>Contact</th>
	</tr>
	<?php
	for($i = 0; $i < count ( $wishlist_array ); $i ++) {
		$wishlist = $wishlist_array [$i];
		?>
	<tr>
		<td><?php echo $wishlist['wishlist_text']?></td>
		<td>
			<?php
		$price_min = $wishlist ['price_min'] ? $wishlist ['price_min'] : 'N/A';
		$price_max = $wishlist ['price_max'] ? $wishlist ['price_max'] : 'N/A';
		echo $price_min . ' - ' . $price_max?>
		</td>
		<td><?php echo explode(" ", $wishlist['recUpdateTime'])[0]?></td>
		<td><button type='button'
				onclick="show_contact_info_div(<?php echo $i?>)">contact</button></td>
	</tr>
	<tr>
		<td colspan='4' bgcolor="#F8F8F8">
			<div id='contact_info_<?php echo $i?>' style="display: none">
			<?php echo $wishlist['contact_info']?>
			</div>
		</td>
	</tr>
	<?php
	}
	?>
</table>

<script type="text/javascript">
<!--
function show_contact_info_div(contact_info_div_id){
	for (var i=0; i<<?php echo count($wishlist_array)?>; i++) {
		if (i == contact_info_div_id)
			$( "#contact_info_" +  i).show( );
		else
			$( "#contact_info_" +  i).hide(  );
	}
}
//-->
</script>
