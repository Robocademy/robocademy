from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from models import Contributor
from django.http import HttpResponse, HttpResponseRedirect
import sys 
from django.shortcuts import render_to_response

def contributors(request):
    return render_to_response('about/contributors.html', {'contributors': Contributor.objects.all()})

def loginuser(request):
    the_user = User.objects.get(username='admin')
    the_user.backend='django.contrib.auth.backends.ModelBackend' 
    login(request, the_user)
    
    return HttpResponseRedirect('/')
    
def createuser(request):
    # appfog doesn't let developers do python manage.py, so you have to code in basic management crap
    return HttpResponse() # so this doesn't work unless the developer wants it to, for creating users on appfog
    username = ''
    password = ''
    email = ''
    if authenticate(username=username, password=password) is not None:
        return HttpResponse("User already created ;)")
    try:
        user = User.objects.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return HttpResponse("User created! :)")
    except:
        print sys.exc_info()[0]
        return HttpResponse("Couldnt\' create user :(")