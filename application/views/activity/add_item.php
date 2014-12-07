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
            action="<?=site_url("activity/add_item/{$activity['Activity_ID']}")?>">

            <div class="form-group">
              <?=form_label("{$red_star}Title", 'title')?>
              <?=form_input('title', set_value('title'), 'class="form-control" placeholder="include Gender &amp; Size"')?>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Picture", 'image_file')?>
              <div id="images_div"></div>
              <span id="image_loading" class="loading"></span>
              <div style="clear: both;"></div>
              <input type="file" id="image_file" class="form-control" />
              <div id="choose_file_unsupport" class="alert alert-info"
                role="alert">If no response when you click "Choose
                File", please click the upper right and choose "Open
                with Browser"</div>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Description", 'description' )?>
              <?=form_textarea('description', set_value('description'), 'class="form-control" placeholder="item condition and other notable things"')?>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Price", 'price')?>
              <div class="input-group">
                <span class="input-group-addon">$</span>
                <?=form_input('price', set_value('price'), 'class="form-control"')?>
              </div>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Condition", 'condition')?>
              <?=form_dropdown('condition', $meta_condition, set_value('condition', 'GD'), 'class="form-control"');?>
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}Email", 'email')?>
              <input type="email" name="email" class="form-control"
                value='<?=set_value('email')?>'
                placeholder="someone@example.com" />
            </div>

            <div class="form-group">
              <?=form_label("{$red_star}ZIP Code", 'zipcode')?>
              <?=form_input('zipcode', set_value('zipcode'), 'class="form-control"')?>
            </div>

            <div class="form-group">
              <?=form_label("WeChat ID", 'wechatId')?>
              <?=form_input('wechatId', set_value('wechatId'), 'class="form-control"')?>
            </div>

            <div class="alert alert-info" role="alert">Please review the
              information carefully.If evey this is correct, click
              Submit below.</div>

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