from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

EMAILREGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9_.+-]+.[a-zA-Z]+$')

# INDEX PAGE
def index(request):
    return render(request, 'our_stories/index.html')

# CREATE NEW USER
def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/')
    else:
        pass_hash = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(username = request.POST['username'], name = request.POST['name'], password = pass_hash.decode('utf-8'))
        request.session['id'] = user.id
        request.session['name'] = user.name
        return redirect('/dash')

def profile(request, id):
    return HttpResponse("Page under conflagration")

def write_story(request, id):
    return HttpResponse("Page under conflagration")

def login(request):
    return render(request, 'our_stories/login.html')

# LOGOUT PROCESS
def logout(request):
    request.session.clear()
    return redirect('/')

# LOGIN PROCESS
def process_login(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/login')
    else:
        user = User.objects.get(username=request.POST['username'])
        if bcrypt.checkpw(request.POST['password'].encode('utf-8'), user.password.encode('utf-8')):
            request.session['id'] = user.id
            request.session['username'] = user.username
            return redirect('/profile')
        else:
            messages.error(request, 'Incorrect password.')
            return redirect('/login')

def write(request):
    return HttpResponse("Page under conflagration")

def explore(request):
    return HttpResponse("Page under conflagration")
