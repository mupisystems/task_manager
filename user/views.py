from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, DetailView, TemplateView
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
    membership = get_object_or_404(Membership, user=request.user, organization=org_id, is_active=True)
   
    user = request.user
    user.org_active = membership.organization 
    user.save()  
    
    request.session['org_active'] = membership.organization.id
    return redirect('home')



class OrgDetailView(DetailView):
  model = Organization
  template_name = 'user/table_member.html'
  context_object_name = 'organization'

  def get_object(self):
      id_org_active_user = self.request.user.org_active.id
      organization = get_object_or_404(Organization, id=id_org_active_user)

      if self.request.user.org_active != organization:
        self.request.user.org_active = organization
        self.request.user.save()
      return organization
  
  def get_role(self):
      id_org_active_user = self.request.user.org_active.id
      organization = get_object_or_404(Organization, id=id_org_active_user)
      membership = Membership.objects.get(user=self.request.user, organization=organization, is_active=True)
      return membership.role
  
  #não sei se pode fazer isso aqui  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    organization = self.get_object()
    context['membership'] = Membership.objects.filter(organization=organization, is_active=True)  
    return context
    
import time  # importa o módulo para usar sleep()

class CreateUserView(CreateView):
    model = CustomUser
    template_name = 'user/add_user_form.html'
    partial_template = 'user/member_row.html'  
    form_class = Userform

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        role = form.cleaned_data['role']

        user = form.save(commit=False)
        user.org_active = self.request.user.org_active
        user.password = 'pbkdf2_sha256$600000$mlkoD4HZEbYrVVaH5oU3Ub$rqttCsLMXJooZRGvXkNXNZzpQlHhi20KcoxpQAnjLks='
        # user.set_password('senha_temporal') 
        user.save()

        member = Membership.objects.create(user=user, organization=self.request.user.org_active, role=role)
        
        if self.request.headers.get('HX-Request'):
            time.sleep(1.5)  # delay de 1.5 segundos antes de responder ao HTMX
            self.template_name = self.partial_template
            return render(self.request, self.template_name, {'member': member})
        else:
            return HttpResponseRedirect(reverse('home'))