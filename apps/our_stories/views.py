from django.shortcuts import render, HttpResponse, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    render(request, 'mainApp/index.html')

def profile(request, id):
    return HttpResponse("Page under conflagration")

def write_story(request, id):
    return HttpResponse("Page under conflagration")

def login(request):
    return HttpResponse("Page under conflagration")

def process_login(request):
    return HttpResponse("Page under conflagration")

def write(request):
    return HttpResponse("Page under conflagration")

def explore(request):
    return HttpResponse("Page under conflagration")
