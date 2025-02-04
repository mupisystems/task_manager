# from django.shortcuts import render, redirect
# from django.http import HttpResponse
# from .forms import UserProfileForm
# from .models import Organization

# def cadastro(request):


#     if request.method == 'POST':
#         form = UserProfileForm(request.POST)

#         password1 = request.POST.get('password1')
#         password2 = request.POST.get('password2')

#         if password1 != password2:
#             return render(request, 'registro.html', {'form': form,'error':'As senhas não coincidem'})

#         if form.is_valid():
#             # owner = UserProfile.objects.filter(email="luiz@gmail.com").first()
#             # org = Organization.objects.filter(owner=owner).first()
#             user = form.save()
#             user.set_password(password1)
#             org = Organization.objects.create(name=f"Organização de {user.username}", owner=user)
#             org.members.add(user)
#             user.organization = org
#             user.save()
#             return HttpResponse("Okay, criado")
#         else:
#             return render(request, 'registro.html', {'form': form})

#     else:
#         form = UserProfileForm()
    
#     return render(request, 'registro.html', {'form': form})



# def showOrganizationMembers(request):
#     # Obtenha a organização do usuário logado
#     user = request.user
#     organization = user.organization

#     # Obtenha membros da organização
#     members = organization.members.all()

#     return render(request, 'members.html', {'members': members})

