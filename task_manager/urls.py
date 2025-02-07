"""
URL configuration for task_manager project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from debug_toolbar.toolbar import debug_toolbar_urls
from task_manager import views
from users import views as vw
from django.contrib.auth.decorators import login_required

urlpatterns = [
                  path('admin/', admin.site.urls),
                  path('accounts/password/change/', login_required(vw.CustomPasswordChangeView.as_view()), name='account_change_password'),
                  path('accounts/', include('allauth.urls')),
                  path('', login_required(views.HomeView.as_view()), name='home'),
                  path('tasks/', include('tasks.urls')),
                  path('user/', include('users.urls')),
                  path('error404', views.Error404View.as_view(), name='erro404'),
                  path('unauthorized', views.Unauthorized.as_view(), name='unauthorized'),
              ] + debug_toolbar_urls()
