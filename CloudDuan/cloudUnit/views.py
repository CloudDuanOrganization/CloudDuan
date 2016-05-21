from django.shortcuts import render,HttpResponse,render_to_response
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from userUnit.models import CdUser
from .models import Duan, Comment, DuanHistory
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
# Create your views here.

def index(request):
    return render_to_response('index.html', {'user': request.user,
                                             'hotList':Duan.objects.order_by('-viewCount')[0:8],
                                             'newestList':Duan.objects.all()[0:8],
                                             'rankList':Duan.objects.order_by('-up')[0:8]})

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
        if request.user.is_authenticated():
            history = DuanHistory()
            history.duan = duan
            history.owner = request.user.cduser
            history.save()
            print('!!!!!!!!!!!!')
        return render_to_response('content.html', {'duan': duan, 'user': request.user})
    else:
        return HttpResponseNotFound('<h1>Page not found</h1>')

@login_required
def duanUp(request):
    if request.method == 'POST':
        duanID = int(request.POST.get('duanID'))
        try:
            print(duanID)
            duan = Duan.objects.get(id__exact=duanID)
            cduser = request.user.cduser
            if (cduser in duan.liker.all()) or (cduser in duan.disliker.all()):
                return JsonResponse({'up_err':'已评价','up_flag':0,'duanUp':duan.up,'duanDown':duan.down})
            duan.up += 1
            duan.liker.add(cduser)
            duan.save()
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
            if (cduser in duan.liker.all()) or (cduser in duan.disliker.all()):
                return JsonResponse({'up_err':'已评价','up_flag':0,'duanUp':duan.up,'duanDown':duan.down})
            duan.down += 1
            duan.disliker.add(cduser)
            duan.save()
            return JsonResponse({'up_err': '踩成功', 'up_flag': 1,'duanUp':duan.up,'duanDown':duan.down})
        except:
            return JsonResponse({'up_err': '段子不存在', 'up_flag': 0})