from django.http import HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, ListView, DetailView
from .forms import Userform
from user.models import CustomUser, Membership, Organization
   
class OrgDetailView(DetailView):
  model = Organization
  template_name = 'details_org.html'
  context_object_name = 'organization'

  def get_object(self):
      # Mudar aqui se for usar Slug
      organization_id = self.kwargs['pk']
      organization = get_object_or_404(Organization, id=organization_id)

      if self.request.user.org_active != organization:
        self.request.user.org_active = organization
        self.request.user.save()
      return organization
  
  def get_role(self):
      # Mudar aqui se for usar Slug
      organization = get_object_or_404(Organization, id=self.kwargs['pk'])
      membership = Membership.objects.get(user=self.request.user, organization=organization, is_active=True)
      return membership.role
      
class CreateUserView(CreateView):
  model = CustomUser
  template_name = 'user/add_user_form.html' 
  form_class = Userform

  def form_valid(self, form):
    """If the form is valid, save the associated model."""
    user = form.save(commit=False)
    user.org_active = self.request.user.org_active
    user.password = '12345678'
    user.save()

    Membership.objects.create(user=user, organization=self.request.user.org_active, role='member')
    return HttpResponseRedirect(reverse('home'))

  
