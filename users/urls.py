
from django.urls import path
from . import views
urlpatterns = [
    # path('registrar/', views.cadastro, name='registro'),
    path('home/', views.CustomLoginView, name='organization_members'),
    path("accounts/signup/", views.CustomSignupView.as_view(), name="account_signup"),
    path("teste/home", views.RegisterNewMemberView.as_view(), name="create_new_member"),
]
