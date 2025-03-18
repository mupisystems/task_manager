from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import CreateView, ListView, DetailView, TemplateView

from .models import Task
from user.models import Membership

class TaskListView(ListView):
  model = Task
  template_name = 'tasks/table_tasks.html'
  context_object_name = 'task'
  
  def get_queryset(self):
    return Task.objects.filter(by_organization=self.request.user.org_active ,visible=True )
    