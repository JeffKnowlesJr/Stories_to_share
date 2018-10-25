from __future__ import unicode_literals
from django.db import models
from datetime import datetime
import re

EMAILREGEX = re.compile(r'^[a-zA-Z0-9.+-]+@[a-zA-Z0-9_.+-]+.[a-zA-Z]+$')

# USER VALIDATION
class UserManager(models.Manager):
    def basic_validator(self, post_data):
        errors = {}
        #USERNAME VALIDATION
        if len(post_data['username']) < 1:
            errors['username'] = 'Username is required.'
        elif len(post_data['username']) < 4:
            errors['username'] = 'Username must be at least 4 characters.'
        elif User.objects.filter(username = post_data['username']):
            errors['username'] = 'Username is already taken, please choose another.'
        #EMAIL VALIDATION
        if len(post_data['email']) < 1:
            errors['email'] = 'Email address is required.'
        elif not EMAILREGEX.match(post_data['email']):
            errors['email'] = 'Valid email address is required.'
        elif User.objects.filter(email = post_data['email']):
            errors['email'] = 'This email address is already associated with another account.'
        #PASSWORD VALIDATION
        if len(post_data['password']) < 1:
            errors['password'] = 'Password is required.'
        elif len(post_data['password']) < 6:
            errors['password'] = 'Password must be at least 6 characters.'
        if post_data['confirm_password'] != post_data['password']:
            errors['password'] = 'Passwords do not match.'
        return errors
    def login_validator(self, post_data):
        errors = {}
        #EMAIL VALIDATION
        if len(post_data["email"]) < 1:
            errors['email'] = 'Email address is required.'
        elif not EMAILREGEX.match(post_data['email']):
            errors['email'] = 'Valid email address is required.'
        elif not User.objects.filter(email = post_data['email']):
            errors['email'] = 'Email address was not found.'
        #PASSWORD VALIDATION
        if len(post_data['password']) < 1:
            errors['password'] = 'Password is required.'
        return errors

class SentenceManager(models.Manager):
    def sentence_validator(self, post_data):
        errors = {}
        #SENTENCE VALIDATION
        if len(post_data['sentence']) < 1:
            errors['sentence'] = 'Sentence is required.'
        elif len(post_data['sentence']) < 4:
            errors['sentence'] = 'Sentence must be at least 2 characters.'

# USER CLASS
class User(models.Model):
    username = models.CharField(max_length = 255)
    email = models.CharField(max_length = 255)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    def __repr__(self):
        return f'User: {self.id} {self.username}'

class Genre(models.Model):
    genre = models.CharField(max_length = 255)

class Story(models.Model):
    users = models.ManyToManyField(User, related_name = "stories")
    genres = models.ManyToManyField(Genre, related_name = "stories")

class Wall(models.Model):
    user = models.ForeignKey(User, related_name="user", on_delete = models.CASCADE)
    stories = models.ManyToManyField(Story, related_name = "walls")

class Sentence(models.Model):
    story = models.ForeignKey(Story, related_name = "sentences", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="sentences", on_delete = models.CASCADE)

class Like(models.Model):
    story = models.ForeignKey(Story, related_name = "likes", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="likes", on_delete = models.CASCADE)

class Trope(models.Model):
    trope = models.CharField(max_length = 255)
    genre = models.ForeignKey(Genre, related_name="tropes", on_delete = models.CASCADE)

class UserTrope(models.Model):
    trope = models.CharField(max_length = 255)
    user = models.ForeignKey(User, related_name="tropes", on_delete = models.CASCADE)
