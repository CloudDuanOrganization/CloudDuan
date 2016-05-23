from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from userUnit.models import CdUser
from cloudUnit.models import DuanMessage
from django.contrib.auth.decorators import login_required

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                request.session.set_expiry(0)
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
        userList = User.objects.filter(email__exact = email)
        if userList:
            return JsonResponse({'register_err': u'邮箱已存在!', 'register_flag': 0})
        try:
            newUser = CdUser()
            newUser.user = User.objects.create_user(username, email, password)
            newUser.save()
            return JsonResponse({'register_err':u'用户注册成功!','register_flag':1})
        except:
            return JsonResponse({'register_err':u'用户已存在!','register_flag':0})
    return HttpResponse('Register Page')

@login_required
def uploadPortrait(request):
    if  (request.method == 'POST'):
        try:
            print('****#####')
            file = request.FILES.get('image')
            print('****#####')
            user = request.user
            print (user, file.name)
            cdUser = user.cduser
            cdUser.portrait = file
            cdUser.save()
            print('*****')
            return HttpResponseRedirect('/userUnit/userProfile/')
        except:
            return HttpResponseRedirect('/userUnit/userProfile/')
            # return False

@login_required
def toUserProfile(request):
    return HttpResponseRedirect('/userUnit/userProfile/userOwn?page=1')

@login_required
def userProfileOwn(request):
    print('#########', request.user)
    page = int(request.GET.get('page'))
    if page <= 0:
        page = 0
    cdUser = request.user.cduser
    return render_to_response(
        "profile.html",
        {'cdUser':cdUser,
        'user':request.user,
        'duanOwn':cdUser.duanOwner.all()[10*(page-1):10*page],
    })

@login_required
def userProfileHistory(request):
    print('#########', request.user)
    page = int(request.GET.get('page'))
    if page <= 0:
        page = 0
    cdUser = request.user.cduser
    return render_to_response("profile.html", {'cdUser':cdUser,
                                               'user':request.user,
                                               'duanHistory':cdUser.duanhistory_set.all()[10*(page-1):10*page],
                                               })

@login_required
def userCollection(request):
    print('#########', request.user)
    page = int(request.GET.get('page'))
    if page <= 0:
        page = 0
    cdUser = request.user.cduser
    return render_to_response("collection.html", {'cdUser':cdUser,
                                               'user':request.user,
                                               'collection':cdUser.collect.all(),
                                               })

@login_required
def userMessageCenter(request):
    cduser = request.user.cduser
    return render_to_response('message.html', {'messageList':cduser.toUser.all()})