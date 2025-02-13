from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Task, Category, Comment
from .forms import TaskForm, CategoryForm, CommentForm
from users.models import MemberShip

# Tarefas (Tasks)
class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'
    context_object_name = 'tasks'

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = self.object.comments.all()
        context['form'] = CommentForm()
        return context

class TaskCreateView(LoginRequiredMixin,CreateView):
    
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_create.html'
    success_url = reverse_lazy('task_list')  # Redireciona para a lista de tarefas após a criação


    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Passa o usuário logado para o form
        return kwargs
    

    # def get_context_data(self, **kwargs):
    #     # context = super().get_context_data(**kwargs)
    #     # return context

    # def form_valid(self, form):
    #     form.instance.created_by = self.request.user  # Atribui o usuário autenticado como criador da tarefa
    #     return super().form_valid(form)

class TaskUpdateView(UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'tasks/task_update.html'
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, 'Tarefa atualizada com sucesso!')
        return super().form_valid(form)

class TaskDeleteView(DeleteView):
    model = Task
    template_name = 'tasks/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Tarefa excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Categorias (Categories)
class CategoryListView(ListView):
    model = Category
    template_name = 'category/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        org = self.request.user.organization
        return Category.objects.filter(created_by=org)

class CategoryCreateView(CreateView):
    model = Category
    form_class = CategoryForm
    template_name = 'category/category_create.html'
    success_url = reverse_lazy('category_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        messages.success(self.request, 'Categoria criada com sucesso!')
        return super().form_valid(form)

class CategoryUpdateView(UpdateView):
    model = Category
    form_class = CategoryForm
    template_name = 'tasks/category_form.html'
    success_url = reverse_lazy('category_list')

    def form_valid(self, form):
        messages.success(self.request, 'Categoria atualizada com sucesso!')
        return super().form_valid(form)

class CategoryDeleteView(DeleteView):
    model = Category
    template_name = 'tasks/category_confirm_delete.html'
    success_url = reverse_lazy('category_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Categoria excluída com sucesso!')
        return super().delete(request, *args, **kwargs)

# Comentários (Comments)
class CommentCreateView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'tasks/task_detail.html'

    def form_valid(self, form):
        task = Task.objects.get(pk=self.kwargs['task_pk'])
        form.instance.task = task
        form.instance.author = self.request.user# Associa o UserProfile do usuário logado
        messages.success(self.request, 'Comentário adicionado com sucesso!')
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('task_detail', kwargs={'pk': self.kwargs['task_pk']})

class CommentDeleteView(DeleteView):
    model = Comment
    template_name = 'tasks/comment_confirm_delete.html'

    def get_success_url(self):
        task_pk = self.object.task.pk
        messages.success(self.request, 'Comentário excluído com sucesso!')
        return reverse_lazy('task_detail', kwargs={'pk': task_pk})