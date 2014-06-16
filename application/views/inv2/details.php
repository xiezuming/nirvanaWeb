<br/>
<?php echo anchor('/inv2', 'Back')?>
<table>
	<tr>
		<th>Id</th>
		<th>Title</th>
		<th>Barcode</th>
		<th>Photo</th>
	</tr>
	<tr>
		<td><?php echo $inv['userId'].'-'.$inv['itemId']?></td>
		<td><?php echo $inv['title']?></td>
		<td><?php echo $inv['barcode']?></td>
		<td>
		<?php 
		if ($inv['photoname1']) {
			$url_orignal = site_url('/inv2/image_orignal/'.$inv['userId'].'/'.$inv['photoname1']);
			$url_thumbnail = site_url('/inv2/image_thumbnail/'.$inv['userId'].'/'.$inv['photoname1']);
			echo '<a href="'.$url_orignal.'" target="_blank"><img src="'.$url_thumbnail.'"/></a>';
		}
		if ($inv['photoname2']) {
			$url_orignal = site_url('/inv2/image_orignal/'.$inv['userId'].'/'.$inv['photoname2']);
			$url_thumbnail = site_url('/inv2/image_thumbnail/'.$inv['userId'].'/'.$inv['photoname2']);
			echo '<a href="'.$url_orignal.'" target="_blank"><img src="'.$url_thumbnail.'"/></a>';
		}
		if ($inv['photoname3']) {
			$url_orignal = site_url('/inv2/image_orignal/'.$inv['userId'].'/'.$inv['photoname3']);
			$url_thumbnail = site_url('/inv2/image_thumbnail/'.$inv['userId'].'/'.$inv['photoname3']);
			echo '<a href="'.$url_orignal.'" target="_blank"><img src="'.$url_thumbnail.'"/></a>';
		}
		?>
		</td>
	</tr>
</table>

<?php echo form_dropdown('category', $categories, NULL, 'onchange="query_items(this.options[this.options.selectedIndex].value)"');?>

<div id='items'></div>
<hr/>
<?php echo form_open('/inv2/link/'.$inv['userId'].'/'.$inv['itemId'], 'id="myform"') ?>
	<input id="linkUrl" name='linkUrl' type="hidden"/>
<?php echo '</form>' ?>

<script type="text/javascript">
function link(url)
{
	document.getElementById("linkUrl").value = url;
	document.forms["myform"].submit();
}
function query_items(catNum)
{
	if (catNum == '') {
		$("#items").html('');
		return;
	}
	
	$.ajax({
		url: "<?php echo site_url('/inv2/query_items/'.$inv['userId'].'/'.$inv['itemId'])?>/" + catNum,
		cache: false,
		success: function(html){
			$("#items").html(html);
		}
	});
}
</script>
