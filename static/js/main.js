$(document).ready(function () {
    // Init
    $('.food_feed').hide();
    $('.grid').hide();
    $('.boxLoading').hide();
});

function removeUpload() {
    $('.file-upload-input').replaceWith($('.file-upload-input').clone());
    $('.file-upload-content').hide();
    $('.image-upload-wrap').show();
    $('.grid').text('');
    $('.grid').hide();
    $('.food_feed').hide();
}

// Upload Preview
function readURL(input) {
    removeUpload();
    if (input.files && input.files[0]) {
        var reader = new FileReader();
        reader.onload = function(e) {
            $('.image-upload-wrap').hide();
            $('.file-upload-image').attr('src', e.target.result);
            $('.file-upload-content').show();
            $('.image-title').html("Remove image");
        };
        reader.readAsDataURL(input.files[0]);
        // Show loading animation
        //$(this).hide();
        $('.boxLoading').show();
        $('.food_feed').fadeIn(50);
        $('.grid').fadeIn(50);
        var formData = new FormData();
        formData.append('file', input.files[0]);
        // Make prediction by calling api /predict
        $.ajax({
            type: 'POST',
            url: '/predict',
            data: formData,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (data) {
                // Get and display the result
                $('.boxLoading').hide();
                $('.grid').append(data);
                console.log('Food!');
                let images = document.querySelectorAll("item");
                console.log(images)
                //lazyload(images);
            },
        });
    } else {
        removeUpload();
    }
};

$('.image-upload-wrap').bind('dragover', function () {
    $('.image-upload-wrap').addClass('image-dropping');
});
$('.image-upload-wrap').bind('dragleave', function () {
    $('.image-upload-wrap').removeClass('image-dropping');
});

function throttle(fn, delay) {
    var last = void 0;
    var timer = void 0;
  
    return function () {
      var now = +new Date();
  
      if (last && now < last + delay) {
        clearTimeout(timer);
  
        timer = setTimeout(function () {
          last = now;
          fn();
        }, delay);
      } else {
        last = now;
        fn();
      }
  
    };
  }
  
  function onScroll() {
    if (window.pageYOffset) {
      $$header.classList.add('is-active');
    } else {
      $$header.classList.remove('is-active');
    }
  }
  
  var $$header = document.querySelector('.js-header');
  
  window.addEventListener('scroll', throttle(onScroll, 25));