from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from .models import Organization
from users import forms
def OrgCreationView(request):
    if request.method != "POST":
        form = forms.OrganizationForm()
    else:
        form = forms.OrganizationForm(request.POST)
        if form.is_valid():
            org = form.save(commit=False)
            org.owner = request.user
            form.save()
            return HttpResponseRedirect(reverse('createorg'))

    context = {'form': form}

    return render(request, 'users/CreateOrg.html', context)