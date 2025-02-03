from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import TaskForm
from .models import Task

class TaskListView(ListView):
    model = Task
    template_name = 'tasks/home.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']


class TaskDetailView(DetailView):
	model = Task
	template_name = 'tasks/details.html'
	context_object_name = 'task'
	pk_url_kwarg = 'custom_pk'


class TaskCreateView(CreateView):
    model = Task
    success_url = reverse_lazy('tasks')
    template_name = 'tasks/create.html'
    form_class = TaskForm

class TaskUpdateView(UpdateView):
    model = Task
    fields = ['title', 'description', 'due_date', 'status']
    success_url = reverse_lazy('tasks')


class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/delete.html'
    context_object_name = 'task'
    pk_url_kwarg = 'custom_pk'