from django.shortcuts import render_to_response, redirect
from django.contrib import auth
from django.core.context_processors import csrf

# Create your views here.
def login(request):
    args = {}
    args.update(csrf(request))
    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            return render_to_response('login.html', args)

    else:
        return render_to_response('login.html', args)


def logout(request):
    auth.logout(request)
    return redirect('/')