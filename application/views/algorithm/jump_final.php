<script>
window.onload = function(){
	document.forms[0].submit();
}
</script>

<?php echo form_open('algorithm/query_item_info_by_similar_item')?>
<?php echo form_hidden('title', $query_title)?>
<?php echo form_hidden('catNum', $catNum)?>
<?php echo form_hidden('similarItemUrl', $similarItemUrl)?>
<?php echo '</form>'?>






