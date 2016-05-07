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
                return render_to_response('signin.html',{'login_err':'登陆成功!'})
            else:
                return render_to_response('signin.html',{'login_err':'账号未激活!'})
        else:
            return render_to_response('signin.html',{'login_err':'登陆失败!'})
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
            return HttpResponse('用户名非法!')
        if (not password) or len(password)<6 or len(password)>40:
            return HttpResponse('密码非法!')
        if password != rePassword:
            return HttpResponse('两次密码不一致!')
        #TODO: Check email format
        try:
            newUser = CdUser()
            newUser.user = User.objects.create_user(username, email, password)
            newUser.save()
            return HttpResponse('用户注册成功!')
        except:
            return HttpResponse('用户已存在!')
    return HttpResponse('Register Page')