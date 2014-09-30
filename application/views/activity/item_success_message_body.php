<?php
$activate_url = site_url ( '/activity/activate_item/' . $b64_item_id );
$edit_url = site_url ( '/activity/edit_item/' . $b64_item_id );
$sold_url = site_url ( '/activity/sold_item/' . $b64_item_id );
?>

<font color="red">IMPORTANT - FURTHER ACTION IS REQUIRED TO COMPLETE
	YOUR REQUEST !!!</font>
<br />
<br />
FOLLOW THE WEB ADDRESS BELOW TO:
<br />
<ul>
	<li>PUBLISH YOUR ITEM</li>
	<li>VERIFY YOUR EMAIL ADDRESS</li>
</ul>
<a href="<?php echo $activate_url?>"><?php echo $activate_url?></a>
<br />
<ul>
	<li>EDIT YOUR ITEM</li>
</ul>
<a href="<?php echo $edit_url?>"><?php echo $edit_url?></a>
<br />
<ul>
	<li>MARK YOUR ITEM AS SOLD</li>
</ul>
<a href="<?php echo $sold_url?>"><?php echo $sold_url?></a>
<br />
<br />
<br />
If not clickable, please copy and paste the address to your browser:
<br />
<br />
<font color="red">THIS LINK IS A PASSWORD. DO NOT SHARE IT</font>
- anyone who has a copy of this link can edit or delete your posting.
<br />
<br />
<font color="red">PLEASE KEEP THIS EMAIL</font>
- you may need it to manage your item!
<br />
<br />
Thanks for using Weee!
