$("#upBtn").click(function() {

    var url = window.location.search;
    var duanID = url.substring(url.lastIndexOf('=') + 1, url.length);

    $.ajax({
        url: '/cloudUnit/duanUp/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID:duanID,
        },
        success: function(data) {
            $("#up").html(data.duanUp)   
        },
        error: function(jqXHR) {
            alert("发生错误：" + jqXHR.status);
        },
    });
});
$("#downBtn").click(function() {

    var url = window.location.search;
    var duanID = url.substring(url.lastIndexOf('=') + 1, url.length);
    $.ajax({
        url: '/cloudUnit/duanDown/',
        type: 'POST',
        dataType: 'json',
        data: {
            duanID:duanID,
        },
        success: function(data) {
            $("#down").html(data.duanDown)
        },
        error: function(jqXHR) {
            alert("发生错误：" + jqXHR.status);
        },
    });
});
