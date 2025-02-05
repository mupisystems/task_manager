from django.contrib.auth.decorators import login_required
from django.urls import  path
from . import views

urlpatterns = [
    path('equipe', login_required(views.showOrgView.as_view()), name='show_org'),
    path('equipe/edit', login_required(views.editEquipeView.as_view()), name='editOrg'),
    path('escolher-equipe', login_required(views.equipeListView.as_view()), name='listar_equipes'),
    path('trocar-perfil/<org_id>/', login_required(views.SwitchEquipeView.as_view()), name='trocar_perfil'),
    path('perfil', login_required(views.mostrar_perfil), name='perfil')

]