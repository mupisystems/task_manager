
from django.urls import path
from . import views
urlpatterns = [
    path('home/', views.ListMembersView.as_view(), name='organization_members'),
    path("signup/", views.CustomSignupView.as_view(), name="account_signup"),
    path("new_member/", views.RegisterNewMemberView.as_view(), name="create_new_member"),
]
