from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('home', views.index),
    path('login', views.login),
    path('logout', views.logout),
    path('process_login', views.process_login),
    path('profile/<int:id>', views.profile),
    path('write', views.write),
    path('write_story/<int:id>', views.write_story),
    path('sentence_process', views.sentence_process),
    path('explore', views.explore),
    path('create', views.create),
    path('write_process', views.write_process)
    ]
