<style>
<!--
img.preview {
	width: 200;
	margin-top: -32;
	border: 1 solid
}

img.close_img {
	float: right;
	cursor: pointer;
	position: relative;
}

div.image_block {
	float: left;
	margin-bottom: 10;
	margin-right: 10;
	width: 200;
}
-->
</style>

<?php $red_star = '<font color="red">*</font>';?>

<div class="container">
  <div class="page-header">
    <h1><?=$activity['Activity_Name']?></h1>
    <p class="lead"><?=$activity['Activity_Desc']?></p>
  </div>

  <div class="content row">
    <div class="col-sm-6 col-sm-offset-3">
      <div id="order_form" class="panel panel-default">
        <div class="panel-body ">
          <?php if ($error || validation_errors()){?>
          <div class="alert alert-danger" role="alert">
            <?=$error?>
            <?=validation_errors()?>
          </div>
          <?php }?>
          
          <form method="post"
            action="<?=site_url("activity/edit_item/{$b64_item_id}")?>">

            <div class="form-group">
              <?=form_label("{$red_star}Title", 'title')?>
              <?=form_input('title', set_value('title', $item['title']), 'class="form-control" placeholder="include Gender &amp; Size"')?>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Picture", 'image_file')?>
              <div id="images_div">
              <?php
              foreach ( $images as $image ) {
               $image_url = $image_url_base . $image ['imageName'];
               $image_url_small = str_replace ( '.jpg', '-360.jpg', $image_url );
               ?>
                <div class="image_block">
                  <img class="close_img"
                    src="<?=base_url ('css/img/close.png')?>"
                    onclick="remove_image_div(this);" /> <img
                    class="preview" src="<?=$image_url_small?>" /> <input
                    type="hidden" name="image_file_names[]"
                    value="<?=$image ['imageName']?>">
                </div>
              <?php }?>
              </div>
              <span id="image_loading" class="loading" />
              <div style="clear: both;"></div>
              <input type="file" id="image_file" class="form-control" />
              <div id="choose_file_unsupport" class="alert alert-info"
                role="alert">If no response when you click "Choose
                File", please click the upper right and choose "Open
                with Browser"</div>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Description", 'description' )?>
              <?=form_textarea('description', set_value('description', $item['desc']), 'class="form-control" placeholder="item condition and other notable things"')?>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Price", 'price')?>
              <div class="input-group">
                <span class="input-group-addon">$</span>
                <?=form_input('price', set_value('price', $item['expectedPrice']), 'class="form-control"')?>
              </div>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Condition", 'condition')?>
              <?=form_dropdown('condition', $meta_condition, set_value('condition', $item['condition']), 'class="form-control"');?>
            </div>

            <fieldset disabled>

              <div class="form-group">
              <?=form_label("Email", 'email')?>
              <?=form_input('', $user['email'], 'class="form-control"')?>
              </div>

              <div class="form-group">
              <?=form_label("ZIP Code", 'zipcode')?>
              <?=form_input('', $user['zipcode'], 'class="form-control"')?>
            </div>

              <div class="form-group">
              <?=form_label("WeChat ID", 'wechatId')?>
              <?=form_input('', $user['wechatId'], 'class="form-control"')?>
            </div>

            </fieldset>

            <button type="submit" class="btn btn-primary">Submit</button>
          </form>

        </div>
      </div>
    </div>
  </div>
</div>

<div id="image_div_template" class="image_block" style="display: none;">
  <img class="close_img" src="<?=base_url ('css/img/close.png')?>"
    onclick="remove_image_div(this);" /> <img class="preview" /> <input
    type="hidden" name="image_data[]" />
</div>


<script type="text/javascript">
var ua = navigator.userAgent.toLowerCase();
if(!(ua.match(/MicroMessenger/i)=="micromessenger" && ua.match(/Android/i)=="android")) {
  $("#choose_file_unsupport").hide();
}

$('#image_loading').hide();

$('#image_file').change(function(event){
  var MAX_LENGTH = 1024;
  console.log(event);

  var input = event.target;
  if (input.files && input.files[0]) {
    $('#image_loading').show();
    var reader = new FileReader();
    reader.onload = function (e) {
      var image = e.target.result;
      var tempImg = new Image();
      tempImg.src = image;
      tempImg.onload = function() {
   
        var tempW = tempImg.width;
        var tempH = tempImg.height;
        if (tempW > tempH) {
            if (tempW > MAX_LENGTH) {
               tempH *= MAX_LENGTH / tempW;
               tempW = MAX_LENGTH;
            }
        } else {
            if (tempH > MAX_LENGTH) {
               tempW *= MAX_LENGTH / tempH;
               tempH = MAX_LENGTH;
            }
        }
        console.log('resize the image to:' + tempW + "*" + tempH);
        
        var canvas = document.createElement('canvas');
        canvas.width = tempW;
        canvas.height = tempH;
        var ctx = canvas.getContext("2d");
        ctx.drawImage(this, 0, 0, tempW, tempH);
        var dataURL = canvas.toDataURL("image/jpeg");

        $('#image_loading').hide();
        var images_div = $('#images_div');
        var image_div = $("#image_div_template").clone().removeAttr("id");
        image_div.children("img.preview").attr('src', dataURL);
        image_div.children("input").attr('value', dataURL);
        image_div.appendTo(images_div);
        image_div.show('slow');

        $('#image_file').val('');
        if (images_div.children().length >= 5) {
          $('#image_file').hide();
        }
      }
      
    };

    reader.readAsDataURL(input.files[0]);
  }
});

function remove_image_div(me) {
  $(me).parent().hide('slow', function() {
    this.remove();
  });
  $('#image_file').show();
}
</script>