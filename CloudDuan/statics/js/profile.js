var PortraitUrl;
//upload image
// function readPortrait(obj) {
//     var file = obj.files[0];
//     //判断类型是不是图片  
//     if (!/image\/\w+/.test(file.type)) {
//         alert("请确保文件为图像类型");
//         return false;
//     }
//     var reader = new FileReader();
//     reader.readAsDataURL(file);
//     reader.onload = function(e) {
//         PortraitUrl = this.result; //base64
//         console.log(PortraitUrl);

//     }
// }

// $(document).ready(function() {
//      //uploadPortrait ajax
//     $("#uploadBtn").click(function() {
//         $.ajax({
//             url: '/userUnit/uploadPortrait/',
//             type: 'POST',
//             data: {
//                 portrait:$("#inputPortrait").val(),
//             },
//             dataType: 'json',
//             success: function() {
//                 alert("修改头像成功!");
//             },
//             error: function(jqXHR) {
//                 alert("发生错误：" + jqXHR.status);
//             },
//         });
//     });

// });