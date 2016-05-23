$(document).ready(function() {
    //summernote init
    $('#summernote2').summernote({
        height: 300,
        minHeight: null,
        maxHeight: null,
        focus: false,
        placeholder: 'write here...'
    });

});
$("#upBtn").click(function() {

    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = subUrl[3];

    $.ajax({
        url: '/cloudUnit/duanUp/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID: duanID,
        },
        success: function(data) {
            $("#up").html(data.duanUp)
        },
        error: function(jqXHR) {
             alert("请登录")
             window.location.href='/userUnit/userLogin/?next=/cloudUnit/duanView/'+duanID+'/';

        },
    });
});
$("#downBtn").click(function() {

    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = subUrl[3];
    $.ajax({
        url: '/cloudUnit/duanDown/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID: duanID,
        },
        success: function(data) {
            $("#down").html(data.duanDown)

        },
        error: function(jqXHR) {
            alert("请登录")
             window.location.href='/userUnit/userLogin/?next=/cloudUnit/duanView/'+duanID+'/';
        },
    });
});
$("#commentBtn").click(function() {
    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = subUrl[3];
    $.ajax({
        url: '/cloudUnit/duanComment/',
        type: 'POST',
        dataType: 'json',
        data: {
            content: $('#summernote2').summernote('code'),
            duanID: duanID,
        },
        success: function(data) {
            if (data.comment_flag === 1) {
                location.reload();
            } else if (data.comment_flag === 0) {
                alert(comment_err);
            }
        },
        error: function(jqXHR) {
            alert("请登录")
            window.location.href='/userUnit/userLogin/?next=/cloudUnit/duanView/'+duanID+'/';
        },
    });
});

$("#collectBtn").click(function() {
    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = subUrl[3];
    $.ajax({
        url: '/cloudUnit/duanCollect/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID: duanID,
        },
        success: function(data) {
            if (data.collect_flag === 1) {
                location.reload();
            }

        },
        error: function(jqXHR) {
            alert(jqXHR)
        },
    });
});


$(function() {
    $('[data-toggle="popover"]').popover()
});
