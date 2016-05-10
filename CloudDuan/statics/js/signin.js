$(function() {
    $('#formbackground').height($(window).height());
    $('#formbackground').width($(window).width());
});


// function checkRegisterForm() {
//     var user = document.RegisterForm.username.value;
//     var pwd1 = document.RegisterForm.password.value;
//     var pwd2 = document.RegisterForm.rePassword.value;
//     if (user.length === 0) {
//         alert("Username should not be null!");
//         document.RegisterForm.username.focus();
//         return false;
//     }
//     if (pwd1 !== pwd2) {
//         alert("password not same");
//         return false;
//     }
//     if (pwd1.length < 6) {
//         alert("password to short")
//         return false;
//     }
//     if (pwd1.length > 40) {
//         alert("password to long")
//         return false;
//     }

// }



$(document).ready(function() {
//如果url中存在锚号,则显示锚号对应的tab
    if (location.hash) {
        $('a[href=' + location.hash + ']').tab('show');
    }
    
 //获取点击的标签的 href   
    $(document.body).on("click", "a[data-toggle]", function(event) {

        location.hash = this.getAttribute("href");

    });
    



});



$(window).on('popstate', function() {

    var anchor = location.hash || $("a[data-toggle=tab]").first().attr("href");

    $('a[href=' + anchor + ']').tab('show');

});
// 处理注册表单
    $("#registerBtn").click(function(){
        $.ajax({
            url: '/userUnit/userRegister/',
            type: 'POST',
            data:{
                username: $("#inputUserName2").val(),
                email: $("#inputEmail").val(),
                password: $("#inputPassword2").val(),
                rePassword: $("#inputRePassword").val(),
            },
            dataType: 'json',    
        success: function(data) {
                if (data.register_flag == 1) {
                    $("#registerResult-success").html(data.register_err);
                    $("#div_registerResult-success").show();
                    $("#div_registerResult-error").hide(); 
                    setTimeout("location.href='/userUnit/userLogin/';", 1000);   
                } else {
                    $("#registerResult-error").html("出现错误：" + data.register_err);
                    $("#div_registerResult-error").show();     
                }  
            },
        error: function(jqXHR,data){     
               alert("发生错误：" + jqXHR.status);
            },  
        });
    });
// 处理登录表单
    $("#loginBtn").click(function(){
        $.ajax({
            url: '/userUnit/userLogin/',
            type: 'POST',
            dataType: 'json',
            data:{
                username:$("#inputUserName").val(),
                password:$("#inputPassword").val(),
            },
        success: function(data) {
                if (data.login_flag == 0) {
                    $("#loginResult-success").html(data.login_err);
                    $("#div_loginResult-success").show();
                    $("#div_loginResult-error").hide();
                    setTimeout("location.href='/home/';", 1000);  
                } else {
                    $("#loginResult-error").html("出现错误：" + data.login_err);
                    $("#div_loginResult-error").show();
                }
                
            },
        error: function(jqXHR){     
               alert("发生错误：" + jqXHR.status);  
            },  
        });

    });
// 单击错误信息的“x”来刷新页面
    $("#close_register_error").click(function(){
        $("#div_registerResult-error").hide();
    });
    $("#close_login_error").click(function(){
        $("#div_loginResult-error").hide();
    });
    