# from django.http import HttpResponseRedirect
from django.core.exceptions import PermissionDenied
from django.template.context_processors import request
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.http import quote_etag
from django.views.generic import ListView, View, DetailView, UpdateView, DeleteView
from users.models import Organization, Membership, User
from django.shortcuts import render, redirect, get_object_or_404


class equipeListView(ListView):
    model = Membership
    template_name = 'users/listar_equipes.html'

    def get_queryset(self):
        queryset = Membership.objects.filter(user=self.request.user)
        return queryset


class SwitchEquipeView(View):
    def get(self, request, org_id):
        organization = get_object_or_404(Organization, id=org_id)
        request.user.current_organization = organization
        request.user.save()
        return redirect('listar_equipes')


class showOrgView(ListView):
    model = Membership
    context_object_name = 'members'
    template_name = 'users/equipe.html'

    def get_queryset(self):
        return Membership.objects.filter(organization=self.request.user.current_organization)


class editEquipeView(UpdateView):
    model = Organization
    fields = ['name']
    template_name = 'users/dashboard_equipe.html'
    context_object_name = 'organization'


    def get_object(self):
        org = get_object_or_404(Organization, id=self.request.user.current_organization.id)
        print(org)
        if org.created_by != self.request.user:
            raise PermissionDenied('Sem Autorização para Isso')
        return org

    def form_valid(self, form):
        organization = form.save(commit=False)
        organization.save()
        return redirect('editOrg')

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     org = self.get_object()
    #     context['memberships'] = Membership.objects.filter(organization=org)
    #     context['roles'] = ['admin', 'owner', 'member']
    #     return context
    #
    # def form_valid(self, form):
    #     organization = form.save(commit=False)
    #     organization.save()
    #
    #     if 'membro_role' in self.request.POST:
    #         membro_id = self.request.POST.get('membro_id')
    #         role = self.request.POST.get('membro_role')
    #         if membro_id:
    #             membro = Membership.objects.get(id=membro_id)
    #             if membro.organization != organization:
    #                 return redirect('unauthorized')
    #             if membro.role == 'owner' and role != 'owner':
    #                 return redirect('unauthorized')
    #             membro.role = role
    #             membro.save()
    #
    #     return redirect('editOrg')


def mostrar_perfil(request):
    user = request.user

    context = {'user': user}

    return render(request, 'users/perfil.html', context)


def remove_confim(request, org_id, remove_target):
    if request.user.profile.current_organizartion != org_id:
        return HttpResponseRedirect(reverse('unauthorized'))
    else:
        user = request.user
        org = org_id
        remove_target = remove_target

        if remove_target.membership.role == 'owner':
            return HttpResponseRedirect(reverse('unauthorized'))
        else:
            context = {'remove_target': remove_target, 'org': org}
            return render(request, 'users/remove_confrm.html', context)
