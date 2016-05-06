from django.shortcuts import render,render_to_response,HttpResponse
from django.contrib.auth import authenticate, login

def userLogin(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            # Redirect to a success page.
            return HttpResponse('Login Successfully!')
        else:
            # Return a 'disabled account' error message
            return HttpResponse('Disabled Account!')

    else:
        # Return an 'invalid login' error message.
        return HttpResponse('Invalid Login!')


