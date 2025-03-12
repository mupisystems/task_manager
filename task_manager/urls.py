from django.contrib import admin
from django.urls import include, path
from django.shortcuts import redirect
from task_manager import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', lambda request: redirect('account_login')),
    path('home/', login_required(views.MyOrgListView.as_view()), name='home'),
    path('home/details_org/<int:pk>/', login_required(views.OrgDetailView.as_view()), name='details_org'),
    path('user/', include('user.urls')),
    #path('tasks/', include('tasks.urls')),
]
# pEi}`#!82u~H5Ik_t@3-) lucas@gmail.com
# d3hfgq5s8jlsd243  murilo@gmail.com