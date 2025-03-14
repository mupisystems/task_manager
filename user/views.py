from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView, DetailView
from .forms import Userform
from user.models import CustomUser, Membership, Organization

class MyOrgsListView(ListView):
    model = Membership
    template_name = 'my_orgs.html'
    context_object_name = 'orgs'

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user, is_active=True)
    
@login_required
def set_active_org(request, org_id):
    membership = get_object_or_404(Membership, user=request.user, organization_id=org_id, is_active=True)
    # Atualiza a organização ativa no usuário
    user = request.user
    user.org_active = membership.organization  # Define a nova organização ativa
    user.save()  # Salva no banco

    # Atualiza a sessão
    request.session['org_active'] = membership.organization.id
    return redirect('home')

class OrgDetailView(DetailView):
  model = Organization
  template_name = 'home.html'
  context_object_name = 'organization'

  def get_object(self):
      # Mudar aqui se for usar Slug
      # organization_id = self.kwargs['pk']
      organization_id = self.request.user.org_active.id
      organization = get_object_or_404(Organization, id=organization_id)

      if self.request.user.org_active != organization:
        self.request.user.org_active = organization
        self.request.user.save()
      return organization
  
  def get_role(self):
      # Mudar aqui se for usar Slug
      organization_id = self.request.user.org_active.id
      organization = get_object_or_404(Organization, id=organization_id)
      membership = Membership.objects.get(user=self.request.user, organization=organization, is_active=True)
      return membership.role
  
  #não sei se pode fazer isso aqui  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    organization = self.get_object()
    context['membership'] = Membership.objects.filter(organization=organization, is_active=True).exclude(role="owner")   
    return context
    
class CreateUserView(CreateView):
  model = CustomUser
  template_name = 'user/add_user_form.html' 
  form_class = Userform

  def form_valid(self, form):
    """If the form is valid, save the associated model."""
    user = form.save(commit=False)
    user.org_active = self.request.user.org_active
    user.password = 'pbkdf2_sha256$600000$mlkoD4HZEbYrVVaH5oU3Ub$rqttCsLMXJooZRGvXkNXNZzpQlHhi20KcoxpQAnjLks='
    user.save()

    Membership.objects.create(user=user, organization=self.request.user.org_active, role='member')
    return HttpResponseRedirect(reverse('home'))
