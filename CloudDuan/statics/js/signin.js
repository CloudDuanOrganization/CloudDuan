$(function(){
$('#formbackground').height($(window).height());
$('#formbackground').width($(window).width());
});


function checkRegisterForm() {
            var user = document.RegisterForm.username.value;
            var pwd1 = document.RegisterForm.password.value;
            var pwd2 = document.RegisterForm.rePassword.value;
            if(user.length===0) {
                alert("Username should not be null!");
                document.RegisterForm.username.focus();
                return false;
            }
            if (pwd1!==pwd2) {
                alert("password not same");
                return false;
            }
            if (pwd1.length<6 ) {
                alert("password to short")
                return false;
            }
            if (pwd1.length>40 ) {
                alert("password to long")
                return false;
            }
            
        }