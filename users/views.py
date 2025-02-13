from urllib import request
from django.shortcuts import render, redirect,get_object_or_404
from django.core.paginator import Paginator
from .forms import CustomSignupForm, RegisterNewMemberForm,CustomLoginForm
from allauth.account.views import SignupView,LoginView
from django.views.generic import ListView, FormView, UpdateView,View
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.core.exceptions import ValidationError
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['organization'] = self.request.user.organization  # Passa a organização para o formulário
        return kwargs

    def form_valid(self, form):
        try:
            form.save()
        except ValidationError as e:
            # Adiciona o erro ao formulário para ser renderizado no template
            form.add_error(None, e)
            return self.form_invalid(form)

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
    paginate_by = 7  # Número de membros por página

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
    
class ChangeUserTeamView(LoginRequiredMixin, ListView):
    model = Organization
    template_name = "change_team.html"
    context_object_name = "organizations"

    def get_queryset(self):
        """Retorna todas as organizações das quais o usuário faz parte"""
        return Organization.objects.filter(org_membership__user=self.request.user)

class UpdateUserOrganizationView(LoginRequiredMixin, View):
    """Atualiza a organização ativa do usuário"""
    def post(self, request, *args, **kwargs):
        org_id = self.kwargs.get("org_id")

        organization = get_object_or_404(Organization, id=org_id)


        # Verifica se o usuário faz parte da organização
        if not MemberShip.objects.filter(user=request.user, organization=organization).exists():
            return HttpResponseForbidden("Você não tem acesso a esta organização.")

        # Atualiza a organização ativa do usuário
        request.user.organization = organization
        request.user.save()

        messages.success(request, f"Agora você está na equipe {organization.name}.")
        return redirect("change_team")  # Redireciona para a lista de equipes