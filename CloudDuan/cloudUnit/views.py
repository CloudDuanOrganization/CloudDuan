from django.shortcuts import render,HttpResponse,render_to_response

# Create your views here.

def index(request):
    return render_to_response('index.html')

def duanPublish(request):
    if request.method == 'POST':
        print(request.body)
        print(str(request.body))
    return HttpResponse('duanPublish')