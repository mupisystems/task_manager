from django.http import HttpResponseRedirect, JsonResponse
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from .models import Task, Comment, Category
from user.models import Membership
from .forms import CreateCategory

class TaskListView(ListView):
  model = Task
  template_name = 'home.html'
  form_class = CreateCategory
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    org_active = self.request.user.org_active
    user = self.request.user
    context['membership'] = Membership.objects.get(user=user, organization=org_active, is_active=True)
    context['tasks_user'] = Task.objects.filter(by_organization=org_active, responsible=user ,visible=True )
    context['tasks_all'] = Task.objects.filter(by_organization=org_active,visible=True )
    context['categories'] = Category.objects.filter(organization=org_active , visible=True )
    # context['cooment'] = Comment.objects.filter()
    return context

class CategoryCreateView(CreateView):
  model = Category
  # template_name = 'user/add_user_form.html'
  # partial_template = 'user/member_row.html'  
  form_class = CreateCategory

  def form_valid(self, form):
    """If the form is valid, save the associated model."""
    category = form.save(commit=False)
    category.organization = self.request.user.org_active
    category.save()