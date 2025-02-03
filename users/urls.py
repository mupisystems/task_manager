from django.contrib import admin
from django.urls import include, path
from users import views

urlpatterns = [
    path('createorg/', views.OrgCreationView, name='createorg')
]