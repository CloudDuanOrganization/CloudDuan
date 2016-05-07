from django.shortcuts import render,render_to_response,HttpResponse
from django.contrib.auth import authenticate, login

def userLogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return render_to_response('signin.html',{'login_err':'Login Successfully!'})
            else:
                # Return a 'disabled account' error message
                return render_to_response('signin.html',{'login_err':'Disabled Account!'})

        else:
            # Return an 'invalid login' error message.
            return render_to_response('signin.html',{'login_err':'Invalid Login!'})
    return render_to_response('signin.html',{})

def userRegister(request):
    if request.method == 'POST':
        pass
    return HttpResponse('Register Page')