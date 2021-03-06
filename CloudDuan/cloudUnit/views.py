from django.shortcuts import render,HttpResponse,render_to_response
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from userUnit.models import CdUser
from .models import Duan, Comment, DuanHistory, DuanMessage, DuanLabel
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from bs4 import BeautifulSoup
from cloudUnit import recommendations
from random import randint
# Create your views here.

def index(request):
    return render_to_response('index.html', {'user': request.user,
                                             'hotList':Duan.objects.order_by('-viewCount', '-id')[0:8],
                                             'newestList':Duan.objects.all().order_by('-id')[0:8],
                                             'rankList':Duan.objects.order_by('-up', '-id')[0:8]})

def hotList(request):
    return render_to_response('hotList.html', {'user': request.user,
                                             'duanList':Duan.objects.order_by('-viewCount', '-id')
                                             }, context_instance=RequestContext(request))

def newestList(request):
    return render_to_response('newest.html', {'user': request.user,
                                             'duanList':Duan.objects.all().order_by('-id'),
                                             }, context_instance=RequestContext(request))

def rankList(request):
    return render_to_response('rankList.html', {'user': request.user,
                                             'duanList':Duan.objects.order_by('-up', '-id')
                                            }, context_instance=RequestContext(request))

def hotView(request, duanID):
    duanList = Duan.objects.order_by('-viewCount', '-id')
    startPage = 1
    for i, d in enumerate(duanList):
        if d.id == int(duanID):
            startPage = i + 1
    page = request.GET.get('page')
    if page:
        page = int(page)
        num = page - 1
    else:
        num = startPage - 1
    duan = duanList[num]
    duan.viewCount += 1
    duan.save()
    print('@@@@@@@')
    if request.user.is_authenticated():
        history = DuanHistory()
        history.duan = duan
        history.owner = request.user.cduser
        history.save()
        print('!!!!!!!!!!!!')
    return render_to_response('pagination.html', {'user': request.user,
                                                'duanList': duanList,
                                                'startPage': startPage,
                                             }, context_instance=RequestContext(request))

def newestView(request, duanID):
    duanList = Duan.objects.all().order_by('-id')
    startPage = 1
    for i,d in enumerate(duanList):
        if d.id == int(duanID):
            startPage = i + 1
    page = request.GET.get('page')
    if page:
        page = int(page)
        num = page - 1
    else:
        num = startPage - 1
    duan = duanList[num]
    duan.viewCount += 1
    duan.save()
    if request.user.is_authenticated():
        history = DuanHistory()
        history.duan = duan
        history.owner = request.user.cduser
        history.save()
        print('!!!!!!!!!!!!')
    return render_to_response('pagination.html', {'user': request.user,
                                             'duanList': duanList,
                                             'startPage': startPage,
                                             }, context_instance=RequestContext(request))

def rankView(request, duanID):
    duanList = Duan.objects.order_by('-up', '-id')
    startPage = 1
    for i, d in enumerate(duanList):
        if d.id == int(duanID):
            startPage = i + 1
    page = request.GET.get('page')
    if page:
        page = int(page)
        num = page - 1
    else:
        num = startPage - 1
    duan = duanList[num]
    duan.viewCount += 1
    duan.save()
    if request.user.is_authenticated():
        history = DuanHistory()
        history.duan = duan
        history.owner = request.user.cduser
        history.save()
        print('!!!!!!!!!!!!')
    return render_to_response('pagination.html', {'user': request.user,
                                             'duanList': duanList,
                                             'startPage': startPage,
                                            }, context_instance=RequestContext(request))

@login_required
def duanPublish(request):
    if request.method == 'POST':
        # 判断标题长度是否合格
        if len(request.POST.get('title')) > 50:
            return JsonResponse({'publish_err':u'标题过长','publish_flag':0})
        # 创建段子，并保存到数据库
        newDuan = Duan()
        newDuan.title = request.POST.get('title')
        newDuan.content = request.POST.get('content')
        # 使用BeautifulSoup将新发布的段子的内容中的纯文本提取出来
        soup = BeautifulSoup(newDuan.content)
        pure = ''
        for i in soup.strings:
            if i is not None:
                pure += i
        newDuan.pureContent = pure
        newDuan.owner = request.user.cduser
        newDuan.image = request.POST.get('cover')
        # 判断是否有封面
        if newDuan.image:
            newDuan.hasCover = True
        # 保存到数据库
        newDuan.save()
        return JsonResponse({'publish_err':u'发布成功','publish_flag':1, 'duan_id': newDuan.id})


def duanView(request, duanID):
    # duanID为要查看的段子的id
    duan = Duan.objects.filter(id__exact=int(duanID)) # 在数据库中查询段子
    if duan: # 如果存在
        duan = duan[0]
        duan.viewCount += 1 # 段子的浏览次数加一
        duan.save()
        hasCollect = True
        hasUp = True
        hasDown = True
        if request.user.is_authenticated(): # 如果用户已登陆
            cduser = request.user.cduser
            history = DuanHistory() # 更新用户浏览记录
            history.duan = duan
            history.owner = request.user.cduser
            history.save()
            hasCollect = (duan in cduser.collect.all()) # 判断用户是否收藏该段子
            hasUp = (duan in cduser.like.all()) # 判断用户是否点赞该段子
            hasDown = (duan in cduser.dislike.all()) # 判断用户是否踩该段子
        # 将数据渲染到前端页面
        return render_to_response('content.html', {'duan': duan, 'user': request.user,
                                                   'duanComment':duan.comment.all(),
                                                   'duanLabel':duan.label.all(),
                                                   'hasUp':hasUp,
                                                   'hasDown':hasDown,
                                                   'hasCollect':hasCollect})
    else:
        # 如果段子id不存在，返回页面没找到
        return HttpResponseNotFound('<h1>Page not found</h1>')

def createDuanMessage(duan, fromUser, toUser, content):
    mess = DuanMessage()
    mess.duan = duan
    mess.fromUser = fromUser
    mess.toUser = toUser
    toUser.newsCount += 1
    mess.content = content
    mess.save()
    toUser.save()
    print('_(:з」∠)__(:з」∠)__(:з」∠)__(:з」∠)_')

@login_required
def duanUp(request):
    if request.method == 'POST':
        duanID = int(request.POST.get('duanID'))
        try:
            print(duanID)
            duan = Duan.objects.get(id__exact=duanID)
            cduser = request.user.cduser
            if (duan in cduser.like.all()) or (duan in cduser.dislike.all()):
                return JsonResponse({'up_err':'已评价','up_flag':0,'duanUp':duan.up,'duanDown':duan.down})
            duan.up += 1
            duan.liker.add(cduser)
            duan.save()
            createDuanMessage(duan, cduser, duan.owner, '赞了')
            return JsonResponse({'up_err': '点赞成功', 'up_flag': 1,'duanUp':duan.up,'duanDown':duan.down})
        except:
            return JsonResponse({'up_err': '段子不存在', 'up_flag': 0})

@login_required
def duanDown(request):
    if request.method == 'POST':
        duanID = int(request.POST.get('duanID'))
        try:
            duan = Duan.objects.get(id__exact=duanID)
            cduser = request.user.cduser
            if ((duan in cduser.like.all()) or (duan in cduser.dislike.all())):
                return JsonResponse({'up_err':'已评价','up_flag':0,'duanUp':duan.up,'duanDown':duan.down})
            duan.down += 1
            duan.disliker.add(cduser)
            duan.save()
            createDuanMessage(duan, cduser, duan.owner, '踩了')
            return JsonResponse({'up_err': '踩成功', 'up_flag': 1,'duanUp':duan.up,'duanDown':duan.down})
        except:
            return JsonResponse({'up_err': '段子不存在', 'up_flag': 0})

@login_required
def duanCollect(request):
    if request.method == 'POST':
        duanID = int(request.POST.get('duanID'))
        try:
            duan = Duan.objects.get(id__exact=duanID)
            cduser = request.user.cduser
            if duan in cduser.collect.all():
                return JsonResponse({'collect_err': '已收藏', 'collect_flag': 0})
            cduser.collect.add(duan)
            cduser.save()
            createDuanMessage(duan, cduser, duan.owner, '收藏了')
            return JsonResponse({'collect_err': '收藏成功', 'collect_flag': 1})
        except:
            return JsonResponse({'collect_err': '段子不存在', 'collect_flag': 0})

@login_required
def duanComment(request):
    if request.method == 'POST':
        duanID = int(request.POST.get('duanID'))
        try:
            duan = Duan.objects.get(id__exact=duanID)
            cduser = request.user.cduser
            comment = Comment()
            comment.content = request.POST.get('content')
            if not comment.content:
                return JsonResponse({'comment_err': '评论内容不得为空', 'comment_flag': 0})
            comment.ofDuan = duan
            comment.owner = cduser
            comment.save()
            createDuanMessage(duan, cduser, duan.owner, '评论了')
            print('@@@@@@@@@@@')
            return JsonResponse({'comment_err': '评论成功', 'comment_flag': 1})
        except:
            return JsonResponse({'comment_err': '段子不存在', 'comment_flag': 0})

def duanList(request):
    return render_to_response('pagination.html',{'duanList':Duan.objects.all()},context_instance=RequestContext(request))

def entry_index(request, template='pagination.html'):
    context = {
        'duanList': Duan.objects.all(),
    }
    return render_to_response(
        template, context, context_instance=RequestContext(request))

def getDict():
    critics = {}
    for u in CdUser.objects.all():
        critics[u] = {}
        for d in u.collect.all():
            critics[u][d] = 4
        for d in u.like.all():
            if d in critics[u]:
                critics[u][d] += 2
            else:
                critics[u][d] = 2
        for d in u.dislike.all():
            if d not in critics[u]:
                critics[u][d] = 0
    return critics

def getRecommendation(user):
    prefDict = getDict()
    itemsim = recommendations.calculateSimilarItems(prefDict)
    return recommendations.getRecommendedItems(prefDict, itemsim, user)

@login_required
def wanderView(request): # 漫步云端功能，可以根据用户的记录给用户推荐适合用户口味的段子。
    cduser = request.user.cduser
    duanList = []
    upList = Duan.objects.order_by('-up')
    simList = getRecommendation(cduser) # 获得段子推荐列表，具体算法见recommendations模块
    for s in simList:
        duanList.append(s[0])
    for s in upList:
        if s not in duanList:
            duanList.append(s)
    page = request.GET.get('page') # 获取漫步云端时的当前页
    if page:
        page = int(page)
        num = page - 1
    else:
        num = 0
    duan = duanList[num]
    duan.viewCount += 1
    duan.save()
    if request.user.is_authenticated():
        history = DuanHistory()
        history.duan = duan
        history.owner = request.user.cduser
        history.save()
    # 将段子进行单页分页渲染，呈现给用户
    return render_to_response('pagination.html', {'user': request.user,
                                                'duanList': duanList,
                                                'startPage': 0,
                                             }, context_instance=RequestContext(request))

def addDuanLabel(request):
    if request.method == 'POST':
        duanID = int(request.POST.get('duanID'))
        try:
            duan = Duan.objects.get(id__exact=duanID)
            label = DuanLabel()
            label.text = request.POST.get('text')
            if not label.text:
                return JsonResponse({'label_err': '标签内容不得为空', 'label_flag': 0})
            print('+++++++++', len(label.text))
            if len(label.text) > 20:
                return JsonResponse({'label_err': '标签内容过长', 'label_flag': 0})
            for l in duan.label.all():
                if l.text == label.text:
                    return JsonResponse({'label_err': '标签已存在', 'label_flag': 0})
            label.ofDuan = duan
            label.colour = randint(1,5)
            label.save()
            return JsonResponse({'label_err': '添加成功', 'label_flag': 1})
        except:
            return JsonResponse({'label_err': '段子不存在', 'label_flag': 0})