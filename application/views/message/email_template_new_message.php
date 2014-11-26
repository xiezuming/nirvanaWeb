Dear <?=$to_user['firstName']?>,<br />
<br />
Someone is interested in your item '<?=$item['title']?>'. The following is the message. To reply, please download the Weee! App from <?=anchor('pages/view/download_app', 'here');?> or reply to <?=$from_user['email']?>.<br/> 
<br/>
Message:
<p style="border:1px solid green; padding: 1em"><?="{$from_user['alias']}: $message_text"?></p>
<br />
Thank you for choosing Weee!
<br />
<br />
The Weee! Team
