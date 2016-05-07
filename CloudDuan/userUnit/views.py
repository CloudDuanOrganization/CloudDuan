from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from userUnit.models import CdUser

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #TODO: Redirect to a success page.
                return render_to_response('signin.html',{'login_err':'登陆成功!', 'login_flag':0})
            else:
                return render_to_response('signin.html',{'login_err':'账号未激活!', 'login_flag':1})
        else:
            return render_to_response('signin.html',{'login_err':'登陆失败!', 'login_flag':2})
    return render_to_response('signin.html',{})

def userLogout(request):
    logout(request)
    return HttpResponse('Logout successfully!')

def userRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        rePassword = request.POST['rePassword']
        if (not username) or len(username)<6 or len(username)>40:
            return render_to_response('signin.html',{'register_err':'用户名非法!','register_flag':0})
        if (not password) or len(password)<6 or len(password)>40:
            return render_to_response('signin.html',{'register_err':'密码非法!','register_flag':0})
        if password != rePassword:
            return render_to_response('signin.html',{'register_err':'两次密码不一致!','register_flag':0})
        #TODO: Check email format
        try:
            newUser = CdUser()
            newUser.user = User.objects.create_user(username, email, password)
            newUser.save()
            return render_to_response('signin.html',{'register_err':'用户注册成功!','register_flag':1})
        except:
            return render_to_response('signin.html',{'register_err':'用户已存在!','register_flag':0})
    return HttpResponse('Register Page')