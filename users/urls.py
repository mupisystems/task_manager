
from django.urls import path
from . import views
urlpatterns = [
    path('registrar/', views.cadastro, name='registro'),
    path('organization/members/', views.showOrganizationMembers, name='organization_members'),
]
