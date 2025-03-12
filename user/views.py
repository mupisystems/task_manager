from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView
from .forms import Userform
from user.models import CustomUser, Membership

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

  
