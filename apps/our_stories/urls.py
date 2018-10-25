from django.conf.urls import url
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('login.html', views.login),
    path('process_login', views.process_login),
    path('profile/<int:id>', views.profile),
    path('write', views.write),
    path('write_story/<int:id>', views.write_story),
    path('explore', views.explore)
    ]
