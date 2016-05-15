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


// function sendFile(file,editor,$editable){
//         var formData = new FormData();
//         formData.append("file", file[0]);
            
//         $.ajax({
//             data: formData,  
//             type: "POST",  
//             url: "/Product/UploadProductDescriptionImage",  
//             cache: false,  
//             contentType: false,  
//             processData: false,  
//             success: function(imageUrl) {  
//                 editor.insertImage($editable, imageUrl);  
//                 //$('.summernote').summernote('editor.insertImage',imageUrl);  
//             },  
//             error: function() {  
                  
//             }  
//         })
//     }


// $('#publish').modal(options)

$(document).ready(function() {
    $('#summernote').summernote({
        height: 300, // set editor height
        minHeight: null, // set minimum height of editor
        maxHeight: null, // set maximum height of editor
        focus: true // set focus to editable area after initializing summernote
        // onImageUpload: function(files, editor, $editable) {
        //         sendFile(files,editor,$editable);
        //     },
    });


    $("#publishBtn").click(function() {

        $.ajax({
            url: '/cloudUnit/duanPublish/',
            type: 'POST',
            dataType: 'json',
            data: {
                title: $("#inputTitle").val(),
                content: $('#summernote').summernote('code'),
            },
            success: function(data) {
                alert("发布成功!");
            },
            error: function(jqXHR) {
                alert("发生错误：" + jqXHR.status);
            },
        });

    });
});
