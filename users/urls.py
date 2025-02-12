
from django.urls import path
from .decorators import *
from . import views

from django.contrib.auth.decorators import user_passes_test

def check_is_manager(user):
    if user.is_anonymous:
        return False
    membership = user.user_membership.filter(organization=user.organization, is_active=True).first()
    return membership.role == 'master' or membership.role == "admin"

urlpatterns = [
    path('home/', views.ListMembersView.as_view(), name='organization_members'),
    path("signup/", views.CustomSignupView.as_view(), name="account_signup"),
    path("new_member/", user_passes_test(check_is_manager,login_url='account_login')(views.RegisterNewMemberView.as_view()), name="create_new_member"),
    path('member/<int:pk>/edit/', views.UpdateUserView.as_view(), name='edit_member'),
    path("change-team/", views.ChangeUserTeamView.as_view(), name="change_team"),
    path("change-team/<int:org_id>/", views.UpdateUserOrganizationView.as_view(), name="update_user_organization"),
]
