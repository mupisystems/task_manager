from django.contrib import admin
from django.urls import include, path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('register', views.registro_user, name='register'),
    path('login', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('equipe/<org_id>', views.show_org, name='show_org'),
    path('equipe/<org_id>/edit', views.edit_org, name='editOrg'),
    path('escolher-equipe/', views.listar_equipes, name='listar_equipes'),
    path('trocar_perfil/<org_id>/', views.switch_profile, name='trocar_perfil'),

]