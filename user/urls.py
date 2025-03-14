from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from task_manager import views
from .views import CreateUserView, MyOrgsListView, set_active_org
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('creat_user/', login_required(CreateUserView.as_view()), name='creat_user'),
    path('my_orgs/', login_required(MyOrgsListView.as_view()), name='my_orgs'),
    path('set_active_org/<int:org_id>/', login_required(set_active_org), name='set_active_org'),
    
]
