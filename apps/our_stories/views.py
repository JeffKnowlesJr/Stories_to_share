from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from random import randint
import bcrypt

# INDEX PAGE
def index(request):
    try:
        print(request.session['id'])
    except KeyError:
        print('no session id')
    return render(request, 'our_stories/index.html')

# CREATE NEW USER
def create(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/login')
    else:
        pass_hash = bcrypt.hashpw(request.POST['password'].encode('utf-8'), bcrypt.gensalt())
        user = User.objects.create(username = request.POST['username'], email = request.POST['email'], password = pass_hash.decode('utf-8'))
        print(user)
        request.session['id'] = user.id
        request.session['username'] = user.username
        return redirect(f'/profile/{user.id}')

def profile(request, id):
    return render(request, 'our_stories/profile.html')

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
            return redirect(f'/profile/{user.id}')
        else:
            messages.error(request, 'Incorrect password.')
            pr('error bad login')
            return redirect('/login')

def write_process(request):
    response = f"{request.POST['group']},{request.POST['story_length']},{request.POST['genre']}"

    #Create a story object
    newStory = Story.objects.create(users= this_user, group=request.POST['group'], story_length = request.POST['story_length'], genre = this_genre)

    this_genre = Genre.objects.get(genre = request.POST['genre'])

    this_user = User.objects.get(request.session['id'])

    newStory.users.add(this_user)

    all_tropes = this_genre.tropes.all()
    trope_range = len(all_tropes)-1
    random_trope = randint(0,trope_range)

    this_trope = this_genre.tropes.get(id = random_trope)

    return render(request, 'our_stories/write_zone.html')

def write(request):
    return render(request, 'our_stories/write_picker.html')

def explore(request):

    return HttpResponse("Page under conflagration")
