from django.contrib import admin
from django.urls import include, path
from . import views
urlpatterns = [
    path('register', views.registro_user, name='register'),
    path('equipe/<org_id>', views.show_org, name='show_org')
]