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
    var duanID = $("#duanID").val();
    var duanType = subUrl[2];

    $.ajax({
        url: '/cloudUnit/duanUp/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID: duanID,
        },
        success: function(data) {
            if(data.up_flag === 0){
                
                $("#upBtn").attr("data-content",data.up_err+",请不要再点了");
                $("#upBtn").attr('title', '停一停');
                $('#upBtn').popover('show')
                // $('#upBtn').popover()
            }
            else if(data.up_flag === 1){
                $("#up").html(data.duanUp)
                
                $("#upBtn").attr("data-content",data.up_err);
                $("#upBtn").attr('title', '恭喜你');
                $('#upBtn').popover('show')
                // $('#upBtn').popover()
            }
        },
        error: function(jqXHR) {
             alert("请登录")
             window.location.href='/userUnit/userLogin/?next=/cloudUnit/'+duanType+'/'+duanID+'/';

        },
    });
});
$("#downBtn").click(function() {

    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = $("#duanID").val();
    var duanType = subUrl[2];
    $.ajax({
        url: '/cloudUnit/duanDown/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID: duanID,
        },
        success: function(data) {
            if(data.up_flag === 0){
                
                $("#downBtn").attr("data-content",data.up_err+",请不要再点了");
                $("#downBtn").attr('title', '停一停');
                $('#downBtn').popover('show')

            }
            else if(data.up_flag === 1){
                $("#down").html(data.duanDown)
                
                $("#downBtn").attr("data-content",data.up_err);
                $("#downBtn").attr('title', '恭喜你');
                $('#downBtn').popover('show')
            }

        },
        error: function(jqXHR) {
            alert("请登录")
             window.location.href='/userUnit/userLogin/?next=/cloudUnit/'+duanType+'/'+duanID+'/';
         },
    });
});
$("#commentBtn").click(function() {
    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = $("#duanID").val();
    var duanType = subUrl[2];

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
                alert(data.comment_err);
            }
        },
        error: function(jqXHR) {
            alert("请登录")
            window.location.href='/userUnit/userLogin/?next=/cloudUnit/'+duanType+'/'+duanID+'/';
        },
    });
});

$("#collectBtn").click(function() {
    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = $("#duanID").val();
    var duanType = subUrl[2];
    $.ajax({
        url: '/cloudUnit/duanCollect/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID: duanID,
        },
        success: function(data) {
            if (data.collect_flag === 1) {
                $("#collectBtn").html("<span class=\"glyphicon glyphicon-star\" id=\"collect\"> </span>已收藏")
            }

        },
        error: function(jqXHR) {
            alert("请登录")
            window.location.href='/userUnit/userLogin/?next=/cloudUnit/'+duanType+'/'+duanID+'/';
        },
    });
});

$("#tagBtn").click(function() {
    var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var duanID = $("#duanID").val();
    var duanType = subUrl[2];
    $.ajax({
        url: '/cloudUnit/addDuanLabel/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID: duanID,
            text:$("#inputTags").val(),
        },
        success: function(data) {
            if (data.label_flag === 1) {
                alert(data.label_err);
                location.reload()
            }
            else{
                alert(data.label_err);
                location.reload()
            }
        },
        error: function(jqXHR) {
            alert("请登录")
            window.location.href='/userUnit/userLogin/?next=/cloudUnit/'+duanType+'/'+duanID+'/';
        },
    });
});


