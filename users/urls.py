from django.contrib.auth.decorators import login_required
from django.urls import  path
from . import views


urlpatterns = [
    path('equipe', login_required(views.ShowOrgView.as_view()), name='mostrar_equipe'),
    path('new-member', login_required(views.CreateMemberView.as_view()), name='criar_membro'),
    path('delete-member/<member_id>/', login_required(views.DeleteMemberView.as_view()), name='delete_membro'),
    path('edit-member/<member_id>/', login_required(views.ManageMemberView.as_view()), name='editar_membro'),
    path('equipe/edit', login_required(views.EditEquipeView.as_view()), name='editOrg'),
    path('escolher-equipe', login_required(views.EquipeListView.as_view()), name='listar_equipes'),
    path('escolher-equipe/<org_id>/', login_required(views.UpdateEquipeView.as_view()), name='trocar_perfil'),
    path('perfil', login_required(views.MostrarPerfilView.as_view()), name='perfil'),

]