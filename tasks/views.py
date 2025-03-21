from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.views.generic import CreateView, ListView, DetailView, TemplateView,UpdateView
from .models import Task, Comment, Category
from user.models import Membership
from .forms import CreateCategory, CreateTask, CreateTaskForOthers, CreateComment
from django.urls import reverse
import time 
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect


User = get_user_model()

class TaskListView(ListView):
  model = Task
  template_name = 'home.html'
  
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
  



class CategoryListView(ListView):
  model = Category
  template_name = 'category/table_category.html'
  form_class = CreateCategory
    
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    org_active = self.request.user.org_active
    context['categories'] = Category.objects.filter(organization=org_active , visible=True )
    return context

class CategoryCreateView(CreateView):
  model = Category
  template_name = 'category/form_category.html'
  partial_template = 'category/row_category.html'  
  form_class = CreateCategory

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['organization'] = self.request.user.org_active
    return kwargs

  def form_valid(self, form):
    """If the form is valid, save the associated model."""
    category = form.save(commit=False)
    category.organization = self.request.user.org_active
    category.save()

    if self.request.headers.get('HX-Request'):
      time.sleep(1.5)
      return render(self.request, 'category/row_category.html', {'category': category})
    else:
      return HttpResponseRedirect(reverse('home'))

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'category/update_form_category.html'
    form_class = CreateCategory  

    def get_queryset(self):
        """Garante que só edite categorias da organização ativa e visíveis."""
        return Category.objects.filter(organization=self.request.user.org_active, visible=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.object  
        return context

    def form_valid(self, form):
        """Ao salvar, verifica se o formulário é válido e salva a categoria existente."""
        category = form.save(commit=False)
        category.organization = self.request.user.org_active  
        category.save()

        if self.request.headers.get('HX-Request'):
            
            return render(self.request, 'category/row_category.html', {'category': category})
        
        return redirect('tasks:category_list')  

class CategoryDeleteView(UpdateView):
    model = Category
    fields = ['visible']  
    template_name = 'category/category_confirm_delete.html'  

    def get_object(self, queryset=None):
        """Recupera a categoria baseada no ID, para garantir que está na organização ativa."""
        return get_object_or_404(Category, pk=self.kwargs['pk'], organization=self.request.user.org_active)

    def form_valid(self, form):
        """Define 'visible' como False e salva a categoria."""
        category = form.save(commit=False)
        category.visible = False  
        category.save()

        if self.request.headers.get('HX-Request'):
            response = HttpResponse(status=204)
            response["X-Category-Id"] = str(category.id)
            return response

        return redirect('tasks:category')

    def form_invalid(self, form):
        """Se o formulário for inválido, retorna erro 404."""
        return HttpResponse(status=404)




class TaskListViewTEMP(ListView):
  model = Task
  template_name = 'table_tasks.html'
  form_class = CreateTask
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    org_active = self.request.user.org_active
    user = self.request.user
    context['tasks_user'] = Task.objects.filter(by_organization=org_active, responsible=user ,visible=True )
    return context   

class TaskCreateView(CreateView):
  model = Task
  template_name = 'tasks/form_tasks.html'
  partial_template = 'tasks/row_tasks.html'  
  form_class = CreateTask

  def get_form_kwargs(self):
    kwargs = super().get_form_kwargs()
    kwargs['org_active'] = self.request.user.org_active
    return kwargs

  def form_valid(self, form):
    """If the form is valid, save the associated model."""
    task = form.save(commit=False)
    task.by_organization = self.request.user.org_active
    task.responsible = self.request.user
    task.save()

    if self.request.headers.get('HX-Request'):
      time.sleep(1.5)
      return render(self.request, self.partial_template, {'task': task})
    else:
      return HttpResponseRedirect(reverse('home'))

class TaskDeleteView(UpdateView):
    model = Task
    fields = ['visible']  
    template_name = 'tasks/confirm_delete_tasks.html'  

    def get_object(self, queryset=None):
        """Recupera a tarefa baseada no ID, para garantir que está na organização ativa."""
        return get_object_or_404(
            Task, 
            pk=self.kwargs['pk'], 
            by_organization=self.request.user.org_active  
        )

    def form_valid(self, form):
        """Define 'visible' como False e salva a tarefa."""
        task = form.save(commit=False)
        task.visible = False  
        task.save()

        if self.request.headers.get('HX-Request'):
            response = HttpResponse(status=204)
            response["X-Task-Id"] = str(task.id)  
            return response

        return redirect('tasks:task_list')  

    def form_invalid(self, form):
        """Se o formulário for inválido, retorna erro 404."""
        return HttpResponse(status=404)


class TaskForOthersListView(ListView):
  model = Task
  template_name = 'table_tasks.html'
  form_class = CreateTask
  
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    org_active = self.request.user.org_active
    user = self.request.user
    context['tasks_user'] = Task.objects.filter(by_organization=org_active, responsible=user ,visible=True )
    return context   

# pedir pra explicar
class TaskCreateForOthersView(CreateView):
    model = Task
    template_name = 'tasks/for_others/form_tasks.html'
    partial_template = 'tasks/for_others/row_tasks.html' 
    form_class = CreateTaskForOthers

    def get_form_kwargs(self):
      kwargs = super().get_form_kwargs()
      kwargs['org_active'] = self.request.user.org_active 
      return kwargs

    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      # adiciona membros da organização no contexto (caso precise)
      context['members'] = User.objects.filter(org_active=self.request.user.org_active)
      return context
    

    def form_valid(self, form):
      task = form.save(commit=False)
      task.by_organization = self.request.user.org_active
      task.save()

      if self.request.headers.get('HX-Request'):
        time.sleep(1.5)
        return render(self.request, self.partial_template, {'task': task})
      else:
        return HttpResponseRedirect(reverse('home'))
    
class CommentCreateView(CreateView):
  model = Comment
  # template_name = 'user/add_user_form.html'
  # partial_template = 'user/member_row.html'  
  form_class = CreateComment

  def form_valid(self, form):
    """If the form is valid, save the associated model."""
    comment = form.save(commit=False)
    comment.create_by = self.request.user
    # comment.task = pegar a task selecionada
    comment.save()
    