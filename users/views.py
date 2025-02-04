from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from .forms import RegistroUser
from .models import Organization, Funcao, UserProfile
from users import forms

def registro_user(request):

    if request.method != "POST":
        form = RegistroUser()
    else:
        form = RegistroUser(request.POST)
        if form.is_valid():
            new_user = form.save()
            organization = Organization.objects.create(name=f'Equipe de {new_user.username}', created_by=new_user)
            Funcao.objects.create(user=new_user, organization=organization, role='owner')
            UserProfile.objects.create(user=new_user, current_organization=organization)
            login(request, new_user)
            return HttpResponseRedirect(reverse('home'))

    context = {'form': form}

    return render(request, 'users/registro.html', context)

def show_org(request, org_id):
    org = get_object_or_404(Organization, id=org_id)
    membros = Funcao.objects.filter(organization=org)

    context = {'org': org, 'membros': membros}

    return render(request, 'users/equipe.html', context)