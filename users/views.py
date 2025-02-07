from django.core.exceptions import PermissionDenied, SuspiciousOperation
from django.http import Http404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, UpdateView, DeleteView, CreateView
from users.models import Organization, Membership, User
from django.shortcuts import redirect, get_object_or_404
from allauth.account.views import PasswordChangeView


class EquipeListView(ListView):
    model = Membership
    template_name = 'users/listar_equipes.html'

    def get_queryset(self):
        queryset = Membership.objects.filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['organizations'] = Membership.objects.filter(user=self.request.user)
        return context


class UpdateEquipeView(UpdateView):
    model = User
    fields = ['current_organization']
    pk_url_kwarg = 'org_id'

    def post(self, request, *args, **kwargs):
        new_org = request.POST.get('organization')
        if new_org:
            user = request.user
            new_org = Organization.objects.filter(id=new_org).first()
            if Membership.objects.filter(organization=new_org, user=user).exists():
                user.current_organization = new_org
                user.save()
            else:
                return redirect('error404')
        else:
            return redirect('error404')

        return redirect('mostrar_equipe')


class ShowOrgView(ListView):
    model = Membership
    context_object_name = 'members'
    template_name = 'users/equipe.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        context['role'] = Membership.objects.filter(user=self.request.user,
                                                    organization=self.request.user.current_organization).first().role

        return context

    def get_queryset(self):
        return Membership.objects.filter(organization=self.request.user.current_organization, is_active=True)


class EditEquipeView(UpdateView):
    model = Organization
    fields = ['name']
    template_name = 'users/dashboard_equipe.html'
    context_object_name = 'organization'

    def get_object(self):
        org = get_object_or_404(Organization, id=self.request.user.current_organization.id)
        if org.created_by != self.request.user:
            raise PermissionDenied('Sem Autorização para Isso')
        return org

    def form_valid(self, form):
        organization = form.save(commit=False)
        organization.save()
        return redirect('editOrg')


class MostrarPerfilView(DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'users/perfil.html'

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

    def get_object(self, queryset=None):
        user = get_object_or_404(User, id=self.request.user.id)
        if queryset is None:
            queryset = self.get_queryset()
        try:
            obj = queryset.get()
        except queryset.model.DoesNotExist:
            raise Http404()

        return obj


class ManageMemberView(UpdateView):
    model = Membership
    fields = ['role']
    pk_url_kwarg = 'member_id'
    template_name = 'users/editar_membro.html'
    context_object_name = 'member'

    def dispatch(self, request, *args, **kwargs):
        user_membership = Membership.objects.filter(user=self.request.user,
                                                    organization=self.request.user.current_organization).first()
        if not user_membership or user_membership.role not in ['admin', 'owner']:
            return redirect('unauthorized')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Membership.objects.filter(user=self.kwargs['member_id'],
                                         organization=self.request.user.current_organization, is_active=True)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            obj = queryset.first()
        if obj is None:
            raise Http404('Usuario não encontrado')

        return obj

    def post(self, request, *args, **kwargs):
        new_role = request.POST.get('role')
        if new_role:
            membership = self.get_queryset().first()
            if membership.role == 'owner':
                raise SuspiciousOperation('O dono não pode se rebaixar no time')
            membership.role = new_role
            membership.save()
        else:
            return redirect('error404')

        return redirect('show_org')


class DeleteMemberView(DeleteView):
    model = Membership
    pk_url_kwarg = 'member_id'
    context_object_name = 'member'
    template_name = 'users/confirm_delete.html'

    def dispatch(self, request, *args, **kwargs):
        user_membership = Membership.objects.filter(user=self.request.user,
                                                    organization=self.request.user.current_organization).first()
        if not user_membership or user_membership.role not in ['admin', 'owner']:
            return redirect('unauthorized')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Membership.objects.filter(user=self.kwargs['member_id'],
                                         organization=self.request.user.current_organization, is_active=True)

    def get_object(self, queryset=None):
        if queryset is None:
            queryset = self.get_queryset()
            obj = queryset.first()
        if obj is None:
            raise Http404('O usuario não existe nessa empresa')

        return obj

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            membership = self.get_object()

            if membership.role == 'owner':
                raise SuspiciousOperation('O dono não pode se expulsar do time')
            else:
                membership.is_active = False
                membership.save()
                return redirect('mostrar_equipe')

class CreateMemberView(CreateView):
    model = User
    template_name = 'users/criar_membro.html'
    fields = ['username', 'email', 'first_name', 'last_name']
    success_url = 'mostrar_equipe'
    context_object_name = 'new_member'


    def form_valid(self, form):
        user = form.save(commit=False)
        user.current_organization = self.request.user.current_organization
        user.password = DEFAULT_PASSWORD
        user.save()
        membership = Membership.objects.create(user=user, organization=self.request.user.current_organization, role='collaborator')
        return redirect('mostrar_equipe')


class CustomPasswordChangeView(PasswordChangeView):
    def get_success_url(self):
        return reverse_lazy('perfil')
