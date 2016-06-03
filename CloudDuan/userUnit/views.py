from django.shortcuts import render, render_to_response, HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from userUnit.models import CdUser
from cloudUnit.models import DuanMessage
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username'] # 获取用户名
        password = request.POST['password'] # 获取密码
        user = authenticate(username=username, password=password) # 用户身份验证
        if user is not None: # 如果用户存在
            if user.is_active: # 如果用户激活
                login(request, user)
                request.session.set_expiry(0) # 设置cookie的保存时间为浏览器关闭后失效
                # 返回JSON值，代表登陆成功。由于使用了AJax，所以使用JsonResponse，下同。
                return JsonResponse({'login_err':u'登陆成功!', 'login_flag':0})
            else:
                # 返回JSON值，代表账号未激活
                return JsonResponse({'login_err':u'账号未激活!', 'login_flag':1})
        else:
            # 返回JSON值，代表登陆失败
            return JsonResponse({'login_err':u'登陆失败!', 'login_flag':2})
    nextUrl = request.GET.get('next', '') # nextUrl指明了登陆成功后跳转的页面
    # 返回渲染后的前端页面
    return render_to_response('signin.html',{'next':nextUrl})

def userLogout(request):
    logout(request)
    return HttpResponseRedirect('/')

def userRegister(request):
    if request.method == 'POST':
        # 获得POST表单的用户信息
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        rePassword = request.POST['rePassword']
        # 判断用户名是否合法
        if (not username) or len(username)<2 or len(username)>40:
            return JsonResponse({'register_err':u'用户名非法!','register_flag':0})
        # 判断密码是否合法
        if (not password) or len(password)<6 or len(password)>40:
            return JsonResponse({'register_err':u'密码非法!','register_flag':0})
        # 判断密码是否一致
        if password != rePassword:
            return JsonResponse({'register_err':u'两次密码不一致!','register_flag':0})
        # 判断邮箱是否存在
        userList = User.objects.filter(email__exact = email)
        if userList: # 判断邮箱存在
            return JsonResponse({'register_err': u'邮箱已存在!', 'register_flag': 0})
        if email.find('@') == -1:
            return JsonResponse({'register_err': u'邮箱格式错误!', 'register_flag': 0})
        try:
            newUser = CdUser()
            # 创建用户，包含用户判断
            newUser.user = User.objects.create_user(username, email, password)
            newUser.save()
            return JsonResponse({'register_err':u'用户注册成功!','register_flag':1})
        except:
            return JsonResponse({'register_err':u'用户已存在!','register_flag':0})
    return HttpResponse('Register Page')


@login_required # 使用装饰器实现用户登陆判断，如果没有登陆则跳转到登录页面，登陆成功后跳转回来。
def uploadPortrait(request):
    if  (request.method == 'POST'):
        try:
            file = request.FILES.get('image') # 在POST中的FILES中获取头像图片
            user = request.user
            cdUser = user.cduser
            cdUser.portrait = file # 用户更改头像
            cdUser.save() # 保存更改到数据库
            return HttpResponseRedirect('/userUnit/userProfile/')
        except:
            return HttpResponseRedirect('/userUnit/userProfile/')

@login_required
def toUserProfile(request):
    return HttpResponseRedirect('/userUnit/userProfile/userOwn/')

@login_required
def userProfileOwn(request):
    print('#########', request.user)
    page = request.GET.get('page')
    if not page:
        page = 0
    else:
        page = int(page)
    if page <= 0:
        page = 0
    cdUser = request.user.cduser
    return render_to_response(
        "profile.html",
        {'cdUser':cdUser,
        'user':request.user,
        'duanOwn':cdUser.duanOwner.all(),
    }, context_instance=RequestContext(request))

@login_required
def userProfileHistory(request):
    print('#########', request.user)
    page = request.GET.get('page')
    if not page:
        page = 0
    else:
        page = int(page)
    if page <= 0:
        page = 0
    cdUser = request.user.cduser
    return render_to_response("profile.html", {'cdUser':cdUser,
                                               'user':request.user,
                                               'duanHistory':cdUser.duanhistory_set.all()[0:150],
                                               }, context_instance=RequestContext(request))

@login_required
def userCollection(request):
    print('#########', request.user)
    page = request.GET.get('page')
    if not page:
        page = 0
    else:
        page = int(page)
    if page <= 0:
        page = 0
    cdUser = request.user.cduser
    return render_to_response("collection.html", {'cdUser':cdUser,
                                               'user':request.user,
                                               'collection':cdUser.collect.all(),
                                               }, context_instance=RequestContext(request))

@login_required
def userMessageCenter(request):
    cduser = request.user.cduser
    messageList = cduser.toUser.all()
    for i in messageList:
        if i.isNew:
            i.isNew = False
    cduser.newsCount = 0
    cduser.save()
    return render_to_response('message.html', {'messageList':cduser.toUser.all()}, context_instance=RequestContext(request))