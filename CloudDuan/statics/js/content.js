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
            alert("发生错误：" + jqXHR.status);
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
            alert("发生错误：" + jqXHR.status);
        },
    });
});

$(function() {
    $('[data-toggle="popover"]').popover()
});
