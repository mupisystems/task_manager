from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import RegistroUser
from users.models import UserProfile, Organization, Membership
from django.shortcuts import render, redirect, get_object_or_404




def registro_user(request):

    if request.method != "POST":
        form = RegistroUser()
    else:
        form = RegistroUser(request.POST)
        if form.is_valid():
            new_user = form.save()
            organization = Organization.objects.create(name=f'Equipe de {new_user.username}', created_by=new_user)
            Membership.objects.create(user=new_user, organization=organization, role='owner')
            UserProfile.objects.create(user=new_user, current_organization=organization)
            login(request, new_user)
            return HttpResponseRedirect(reverse('home'))

    context = {'form': form}

    return render(request, 'users/registro.html', context)



@login_required
def listar_equipes(request):

    perfis = UserProfile.objects.filter(user=request.user)

    org_atual_id = request.session.get('organization_id')

    context = {'perfis': perfis,'org_atual_id': org_atual_id
    }

    return render(request, 'users/listar_equipes.html', context)




@login_required
def switch_profile(request, org_id):



    user_profile = get_object_or_404(UserProfile, user=request.user, current_organization_id=org_id)


    request.session['organization_id'] = org_id


    return redirect('home')


@login_required()
def show_org(request, org_id):

    org = get_object_or_404(Organization, id=org_id)
    current_org = request.session.get('organization_id')
    if current_org != org_id:
        return HttpResponseRedirect(reverse('erro404'))

    membros = Membership.objects.filter(organization=org)
    user_role = Membership.objects.filter(organization=current_org, user=request.user)


    context = {'org': org, 'membros': membros, 'user_role': user_role}

    return render(request, 'users/equipe.html', context)

@login_required()
def edit_org(request, org_id):

    user_profile = UserProfile.objects.filter(user=request.user).first()

    user_func = Membership.objects.filter(organization=user_profile.current_organization, user=request.user).first()
    print(user_func.role)
    current_org = request.session.get('organization_id')
    if user_func (user_func.role =='owner' or user_func.role == 'admin'):
       org = get_object_or_404(Organization, id=org_id)
       membros = Membership.objects.filter(organization=org)
       user_role = Membership.objects.filter(organization=current_org, user=request.user)
    else:
        return HttpResponseRedirect(reverse('erro404'))

    context = {'org': org, 'membros': membros, 'user_role': user_role, 'user': request.user}

    return render(request, 'users/edit_org.html', context)