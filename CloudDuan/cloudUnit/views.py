from django.shortcuts import render,HttpResponse,render_to_response
from userUnit.models import CdUser
from .models import Duan, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render_to_response('index.html', {'user': request.user})

@login_required
def duanPublish(request):
    if request.method == 'POST':
        # print(request.body)
        # print(str(request.body))
        print(request.POST.get('title'))
        print(request.POST.get('content'))
        newDuan = Duan()
        newDuan.title = request.POST.get('title')
        newDuan.content = request.POST.get('content')
        newDuan.owner = request.user.cduser
        newDuan.save()
        
        return HttpResponse(newDuan.content)

        # imageList = request.FILES.getlist('multipleFileUpload')
        # for i in imageList:
        #     print(i.name)
        # return HttpResponse(request.POST['content'])
        #  return HttpResponse()