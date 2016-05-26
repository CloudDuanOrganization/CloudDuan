from django.shortcuts import render,HttpResponse,render_to_response
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from userUnit.models import CdUser
from .models import Duan, Comment, DuanHistory, DuanMessage
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    return render_to_response('index.html', {'user': request.user,
                                             'hotList':Duan.objects.order_by('-viewCount')[0:8],
                                             'newestList':Duan.objects.all()[0:8],
                                             'rankList':Duan.objects.order_by('-up')[0:8]})

def hotList(request):
    return render_to_response('hotList.html', {'user': request.user,
                                             'duanList':Duan.objects.order_by('-viewCount')
                                             }, context_instance=RequestContext(request))

def newestList(request):
    return render_to_response('newest.html', {'user': request.user,
                                             'duanList':Duan.objects.all(),
                                             }, context_instance=RequestContext(request))

def rankList(request):
    return render_to_response('rankList.html', {'user': request.user,
                                             'duanList':Duan.objects.order_by('-up')
                                            }, context_instance=RequestContext(request))

def hotView(request, duanID):
    duanList = Duan.objects.order_by('-viewCount')
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
    duanList = Duan.objects.all()
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
    duanList = Duan.objects.order_by('-up')
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
        # print(request.body)
        # print(str(request.body))
        # print(request.POST.get('title'))
        # print(request.POST.get('content'))
        # print('###########')
        # print(len(request.POST.get('title')))
        if len(request.POST.get('title')) > 50:
            return JsonResponse({'publish_err':u'标题过长','publish_flag':0})
        newDuan = Duan()
        newDuan.title = request.POST.get('title')
        newDuan.content = request.POST.get('content')
        soup = BeautifulSoup(newDuan.content)
        print('$$$$$$$$$$$$$$$')
        pure = ''
        for i in soup.strings:
            print('*************',i,type(i))
            if i is not None:
                pure += i
                print('@@@@@@@@@@@@@@',i)
        newDuan.pureContent = pure
        print(pure)
        newDuan.owner = request.user.cduser
        # newDuan.image = request.FILES['cover']
        newDuan.image = request.POST.get('cover')
        if newDuan.image:
            newDuan.hasCover = True
        newDuan.save()
        return JsonResponse({'publish_err':u'发布成功','publish_flag':1, 'duan_id': newDuan.id})

        # imageList = request.FILES.getlist('multipleFileUpload')
        # for i in imageList:
        #     print(i.name)
        # return HttpResponse(request.POST['content'])
        #  return HttpResponse()

def duanView(request, duanID):
    # duanID = request.GET.get('duanID')
    duan = Duan.objects.filter(id__exact=int(duanID))
    if duan:
        duan = duan[0]
        duan.viewCount += 1
        duan.save()
        hasCollect = True
        hasUp = True
        hasDown = True
        if request.user.is_authenticated():
            cduser = request.user.cduser
            history = DuanHistory()
            history.duan = duan
            history.owner = request.user.cduser
            history.save()
            print('!!!!!!!!!!!!')
            hasCollect = (duan in cduser.collect.all())
            hasUp = (duan in cduser.like.all())
            hasDown = (duan in cduser.dislike.all())
        return render_to_response('content.html', {'duan': duan, 'user': request.user,
                                                   'duanComment':duan.comment.all(),
                                                   'hasUp':hasUp,
                                                   'hasDown':hasDown,
                                                   'hasCollect':hasCollect})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

def createDuanMessage(duan, fromUser, toUser, content):
    mess = DuanMessage()
    mess.duan = duan
    mess.fromUser = fromUser
    mess.toUser = toUser
    mess.content = content
    mess.save()
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
        critics[u.id] = {}
        for d in u.collect.all():
            critics[u.id][d.id] = 4
        for d in u.like.all():
            if d.id in critics[u.id]:
                critics[u.id][d.id] += 2
            else:
                critics[u.id][d.id] = 2
        for d in u.dislike.all():
            if d.id not in critics[u.id]:
                critics[u.id][d.id] = 0
    return critics
