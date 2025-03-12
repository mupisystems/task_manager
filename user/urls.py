from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from task_manager import views
from .views import CreateUserView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('creat_user/', login_required(CreateUserView.as_view()), name='creat_user'),
]
