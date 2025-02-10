from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import CustomSignupForm, RegisterNewMemberForm
from allauth.account.views import SignupView,FormView
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

class RegisterNewMemberView(LoginRequiredMixin, SignupView):
    form_class = RegisterNewMemberForm
    success_url = reverse_lazy("organization_members")

    def form_valid(self, form):
        # Cria o usuário e associa à organização
        user = form.save(self.request)
        
        # Associa à organização do usuário logado
        user.organization = self.request.user.organization
        user.save()
        
        # Cria o vínculo como membro
        MemberShip.objects.create(
            user=user,
            organization=user.organization,
            role='member'
        )
        
        return super().form_valid(form)

def CustomLoginView(request):

    # buscar todos os membros dentro de uma equipe
    members = MemberShip.objects.filter(organization=request.user.organization)



    print(members)
    return render(request, 'members.html',{'membros':members})
    

