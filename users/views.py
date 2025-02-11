from urllib import request
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .forms import CustomSignupForm, RegisterNewMemberForm,CustomLoginForm
from allauth.account.views import SignupView,LoginView
from django.views.generic import ListView, FormView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from .models import Organization, MemberShip,UserProfile
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


class ListMembersView(LoginRequiredMixin, ListView):
    model = MemberShip
    template_name = 'home.html'
    context_object_name = 'members'
    paginate_by = 10  # Número de membros por página

    def get_queryset(self):
        # Filtra apenas os membros da mesma organização e ordena por nome de usuário
        return MemberShip.objects.filter(
            organization=self.request.user.organization
        ).order_by('user__username')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, self.paginate_by)
        page = self.request.GET.get('page')
        members = paginator.get_page(page)
        is_admin = MemberShip.objects.filter(
            user=self.request.user, 
            organization=self.request.user.organization,
            role="admin"
        ).exists()

        context['members'] = members
        context['is_admin'] = is_admin
        return context
    

class UpdateUserView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = MemberShip
    fields = ['role']
    template_name = 'edit_member.html'
    success_url = reverse_lazy('organization_members')

    # Verifica se o usuário tem permissão
    def test_func(self):
        membership = self.get_object()
        return (
            self.request.user == membership.organization.owner
            or MemberShip.objects.filter(user=self.request.user, organization=self.request.user.organization, role='admin').exists()
            ) # Dono ou administrador pode atualizar membros


    # Opcional: Restringe a queryset para membros da mesma organização
    def get_queryset(self):
        if self.request.user == self.request.user.organization.owner or MemberShip.objects.filter(user=self.request.user, organization=self.request.user.organization, role='admin').exists():
            return MemberShip.objects.filter(organization=self.request.user.organization)
        print('por isso mesmo')
        return MemberShip.objects.none()
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        form.fields['role'].choices = [
            ('admin', 'Administrador'),
            ('member', 'Colaborador')
        ]
        return form