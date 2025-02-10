from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomSignupForm, RegisterNewMemberForm,CustomLoginForm
from allauth.account.views import SignupView,LoginView
from django.views.generic import ListView, FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from .models import Organization, MemberShip
from django.contrib import messages


class CustomSignupView(SignupView):
    form_class = CustomSignupForm  
    success_url = reverse_lazy("organization_members") 

    def form_valid(self, form):
        response = super().form_valid(form)
        # self.request.session["welcome_message"] = f"Bem-vindo, {form.cleaned_data['username']}!"
        messages.success(self.request, f"Obrigado por se cadastrar. Agora vocé poderá fazer login.")
        return response

class RegisterNewMemberView(LoginRequiredMixin, FormView):
    form_class = RegisterNewMemberForm
    success_url = reverse_lazy("organization_members")
    template_name = 'new_member.html'

    def form_valid(self, form):
        # Cria o usuário e associa à organização
        user = form.save(self.request)
        print('testeeee')
        
        role = form.cleaned_data.get('role','member')
        
        # Associa à organização do usuário logado
        user.organization = self.request.user.organization
        user.save()
        
        # Cria o vínculo como membro
        MemberShip.objects.create(
            user=user,
            organization=user.organization,
            role=role
        )
        
        return super().form_valid(form)

class CustomLoginView(LoginView):
    form_class = CustomLoginForm
    template_name = 'login.html'
    success_url = reverse_lazy('organization_members')

    def form_valid(self, form):
        self.request.session["welcome_message"] = f"Bem-vindo, {form.cleaned_data['login']}!"
        return super().form_valid(form)


class ListMembersView(ListView):
    model = MemberShip
    template_name = 'home.html'
    context_object_name = 'members'

    def get_queryset(self):
        return MemberShip.objects.filter(organization=self.request.user.organization)
