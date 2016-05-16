
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
                cover: $('#inputCover').val(),
            },
            dataType: 'json',
            success: function() {
                alert("发布成功!");
            },
            error: function(jqXHR) {
                alert("发生错误：" + jqXHR.status);
            },
        });
    });
    //upload image
    

});
