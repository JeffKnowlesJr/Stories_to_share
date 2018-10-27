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

def write(request):
    
    return render(request, 'our_stories/write_picker.html')


def write_process(request):

    #Create a story object

    print("Executing write process")

    this_genre = Genre.objects.get(genre = request.POST['genre'])
    print("The genre chosen is: ", this_genre.genre)

    this_user = User.objects.get(id = request.session['id'])
    print("This user is: ", this_user.username)

    # newStory = Story.objects.create(users= this_user, group=request.POST['group'], story_length = request.POST['story_length'], genre = this_genre)

    # newStory.users.set(this_user)

    all_tropes = this_genre.tropes.all()

    trope_range = len(all_tropes)-1
    random_trope = randint(0,trope_range)

    this_trope = this_genre.tropes.get(id = random_trope).trope

    request.session['trope'] = this_trope

    print(this_trope)

    context = {
        "trope":request.session['trope']
    }

    return render(request, 'our_stories/write_zone.html',context)


def explore(request):

    return HttpResponse("Page under conflagration")
