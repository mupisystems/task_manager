from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TaskForm
from teams.models import Membership
from .models import Task

# ----------------------------------------
class TaskListView(ListView):
    model = Task
    context_object_name = 'tasks'
    template_name = 'tasks/task_list.html'
    paginate_by = 8

    def get_queryset(self):
        user = self.request.user
        if user.current_team:
            membership = Membership.objects.filter(members=user, team=user.current_team).first()
            if membership:
                user_type = membership.user_type
                if user_type == 'Proprietário' or user_type == 'Administrador':
                    return Task.objects.filter(team=user.current_team)
                else:
                    return Task.objects.filter(team=user.current_team, member__members=user)
        return Task.objects.none()

class TaskCreateView(CreateView):
    template_name = 'tasks/task_create.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('task_list')


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task' 

