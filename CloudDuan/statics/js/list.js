$(document).ready(function(){
	var url = document.location.toString();
    var arrUrl = url.split("//");
    var subUrl = arrUrl[1].split("/");
    var listType = subUrl[2];



    if (listType === 'hotList'){
    	$("#listTitle").html("<img src=\"/static/images/icon－热门推荐.png\">&nbsp;热门推荐</a>");

    }
    if (listType === 'newestList'){
    	$("#listTitle").html("<img src=\"/static/images/icon－新鲜段子.png\"> &nbsp;新鲜段子</a>")

    }
    if (listType === 'rankList'){
    	$("#listTitle").html("<img src=\"/static/images/icon－排行榜.png\"> &nbsp;排行榜</a>")

    }
});


