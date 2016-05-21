$(function() {
    $(window).scroll(function() {
        if ($(window).scrollTop() >= 100) { //向下滚动像素大于这个值时，即出现小火箭~
            $('.actGotop').fadeIn(300); //火箭淡入的时间，越小出现的越快~
        } else {
            $('.actGotop').fadeOut(300); //火箭淡出的时间，越小消失的越快~
        }
    });
    $('.actGotop').click(function() { $('html,body').animate({ scrollTop: '0px' }, 800); }); //火箭动画停留时间，越小消失的越快~
});

var coverUrl;
//upload image
function readFile(obj) {
    var file = obj.files[0];
    //判断类型是不是图片  
    if (!/image\/\w+/.test(file.type)) {
        alert("请确保文件为图像类型");
        return false;
    }
    var reader = new FileReader();
    reader.readAsDataURL(file);
    reader.onload = function(e) {
        coverUrl = this.result; //base64
        // console.log(coverUrl);

    }
}


$(document).ready(function() {

    //summernote init
    $('#summernote').summernote({
        height: 300,
        minHeight: null,
        maxHeight: null,
        focus: true
    });



    //publish duan ajax
    $("#publishBtn").click(function() {
        $.ajax({
            url: '/cloudUnit/duanPublish/',
            type: 'POST',
            data: {
                title: $("#inputTitle").val(),
                content: $('#summernote').summernote('code'),
                cover: coverUrl,
            },
            dataType: 'json',
            success: function(data) {
                window.location.href="/cloudUnit/duanView/"+data.duan_id
            },
            error: function(jqXHR) {
                alert("发生错误：" + jqXHR.status);
            },
        });
    });


});
