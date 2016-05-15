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
                } else if(data.register_flag == 0) {
                    $("#registerResult-error").html(data.register_err);
                    $("#p_registerResult-error").html("请检查自己的输入。")
                    
                    $("#div_registerResult-success").hide();
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
                var url = window.location.search;
                if(url){
                    nextUrl = url.substring(url.lastIndexOf('=')+1, url.length);
                }else {
                    nextUrl = '/';
                }
                
                if (data.login_flag == 0) {
                    $("#loginResult-success").html(data.login_err);
                    $("#div_loginResult-success").show();
                    $("#div_loginResult-error").hide();
                    setTimeout("top.location.href='"+nextUrl+"';", 1000);  
                    // console.log(data.login_flag)
                    // console.log(data.login_err)
                } else if(data.login_flag == 2) {
                    $("#loginResult-error").html(data.login_err);
                    $("#p_loginResult-error").html("请检查自己的帐号密码。")
                    $("#div_loginResult-error").show();
                    $("#pbtn_loginResult-error").show();
                    $("#div_loginResult-success").hide();
                }else{
                    $("#loginResult-error").html(data.login_err);
                    $("#p_loginResult-error").html("请前去验证邮箱。")
                    $("#div_loginResult-error").show();
                    $("#div_loginResult-success").hide();
                    $("#pbtn_loginResult-error").hide();
                }
                
            },
        error: function(jqXHR){     
               alert("发生错误：" + jqXHR.status);  
            },  
        });

    });
/** 
*单击警告框的“x”来隐藏警告框
**/
    $("#close_register_error").click(function(){
        $("#div_registerResult-error").hide();
    });
    $("#close_login_error").click(function(){
        $("#div_loginResult-error").hide();
    });
    $("#close_register_success").click(function(){
        $("#div_registerResult-success").hide();
    });
    $("#close_login_success").click(function(){
        $("#div_loginResult-success").hide();
    });
    