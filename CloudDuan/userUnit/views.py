from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from userUnit.models import CdUser
from django.contrib.auth.decorators import login_required

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'login_err':u'登陆成功!', 'login_flag':0})
            else:
                return JsonResponse({'login_err':u'账号未激活!', 'login_flag':1})
        else:
            return JsonResponse({'login_err':u'登陆失败!', 'login_flag':2})
    nextUrl = request.GET.get('next', '')
    print('---->', nextUrl)
    return render_to_response('signin.html',{'next':nextUrl})

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/')

def userRegister(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        rePassword = request.POST['rePassword']
        if (not username) or len(username)<2 or len(username)>40:
            return JsonResponse({'register_err':u'用户名非法!','register_flag':0})
        if (not password) or len(password)<6 or len(password)>40:
            return JsonResponse({'register_err':u'密码非法!','register_flag':0})
        if password != rePassword:
            return JsonResponse({'register_err':u'两次密码不一致!','register_flag':0})
        #TODO: Check email format
        try:
            newUser = CdUser()
            newUser.user = User.objects.create_user(username, email, password)
            newUser.save()
            return JsonResponse({'register_err':u'用户注册成功!','register_flag':1})
        except:
            return JsonResponse({'register_err':u'用户已存在!','register_flag':0})
    return HttpResponse('Register Page')

def uploadPortrait(request):
    if  (request.method == 'POST'):
        try:
            file = request.FILES['portrait']
            user = request.user
            print (user, file.name)
            cdUser = user.cduser
            cdUser.portrait = file
            cdUser.save()
            print('*****')
            return True
        except:
            return False

@login_required
def userProfile(request):
    print('#########', request.user)
    cdUser = request.user.cduser
    return render_to_response("profile.html", {'cdUser':cdUser})