from django.shortcuts import render,HttpResponse,render_to_response
from django.http import JsonResponse
from django.http import HttpResponseNotFound
from userUnit.models import CdUser
from .models import Duan, Comment, DuanHistory
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render_to_response('index.html', {'user': request.user})

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
        newDuan.owner = request.user.cduser
        # newDuan.image = request.FILES['cover']
        newDuan.image = request.POST.get('cover')
        newDuan.save()
        return JsonResponse({'publish_err':u'发布成功','publish_flag':1, 'duan_id': newDuan.id})

        # imageList = request.FILES.getlist('multipleFileUpload')
        # for i in imageList:
        #     print(i.name)
        # return HttpResponse(request.POST['content'])
        #  return HttpResponse()

def duanView(request):
    duanID = request.GET.get('duanID')
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