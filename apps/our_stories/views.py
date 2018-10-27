from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
from random import randint
import bcrypt

# INDEX PAGE
def index(request):
    print("\n<<--------------Rendering home page-------------->>\n")

    try:
        print(request.session['id'])
    except KeyError:
        print('no session id')
    return render(request, 'our_stories/index.html')

# CREATE NEW USER
def create(request):
    print("\n<<--------------Executing new user process-------------->>\n")

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
    print("\n<<--------------Rendering Profile-------------->>\n")

    return render(request, 'our_stories/profile.html')

def write_story(request, id):
    print("\n<<--------------Executing write process-------------->>\n")

    return HttpResponse("Page under conflagration")

def login(request):
    print("\n<<--------------Rendering Login-------------->>\n")

    return render(request, 'our_stories/login.html')

# LOGOUT PROCESS
def logout(request):
    print("\n<<--------------Logged Out-------------->>\n")

    request.session.clear()
    return redirect('/')

# LOGIN PROCESS
def process_login(request):
    print("\n<<--------------Executing login process-------------->>\n")

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
    print("\n<<--------------Rendering write page-------------->>\n")
    
    return render(request, 'our_stories/write_picker.html')


def write_process(request):
    print("\n<<--------------Executing write process-------------->>\n")

    #Create a genre object
    this_genre = Genre.objects.get(genre = request.POST['genre'])
    print("The genre chosen is: ", this_genre.genre)

    #Create a user object
    this_user = User.objects.get(id = request.session['id'])
    print("This user is: ", this_user.username)

    #Create a story object
    this_story = Story.objects.create(group=request.POST['group'], story_length = request.POST['story_length'])

    this_story.genres.add(this_genre)
    this_story.users.add(this_user)

    print("CREATED NEW STORY: ", this_story)

    #Generate a random trope
    all_tropes = this_genre.tropes.all()

    trope_range = len(all_tropes)-1
    random_trope = randint(0,trope_range)

    this_trope = this_genre.tropes.get(id = random_trope).trope

    #Store random trope in session
    request.session['trope'] = this_trope

    print(this_trope)

    context = {
        "trope":request.session['trope']
    }

    return render(request, 'our_stories/write_zone.html',context)


def explore(request):

    return HttpResponse("Page under conflagration")
