from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.http import Http404
from users.models import Membership
from .models import Task, Category, Comments


class TaskCreateView(CreateView):
    model = Task
    fields = ['title', 'description', 'category', 'user']
    template_name = 'tasks/task_create.html'


    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        queryset = Membership.objects.filter(organization=self.request.user.current_organization)
        form.fields['user'].queryset = queryset
        form.fields['user'].label_from_instance = lambda obj: f"{obj.user.first_name} - {obj.get_role_display()}"

        form.fields['category'].queryset = queryset
        return form

    def form_valid(self, form):
        task = form.save(commit=False)
        task.organization = self.request.user.current_organization
        task.created_by = self.request.user
        task.save()
        return redirect('mostrar_tarefas')


class TaskListView(ListView):
    model = Task
    template_name = 'tasks/task_list.html'

    def get_queryset(self):
        queryset = Task.objects.filter(organization=self.request.user.current_organization, is_active=True)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        role = Membership.objects.filter(user=self.request.user,
                                         organization=self.request.user.current_organization).first().role
        if role in ['owner', 'admin']:
            context['tasks'] = Task.objects.filter(organization=self.request.user.current_organization,
                                                   is_active=True).first()
            print('cinco')
        else:
            context['tasks'] = Task.objects.filter(user=self.request.user,
                                                   organization=self.request.user.current_organization,
                                                   is_active=True).first()

        return context


class MostrarTaskView(ListView):
    model = Task
    template_name = 'tasks/task.html'

    def get_queryset(self):
        queryset = Task.objects.filter(id=self.kwargs['task_id'], organization=self.request.user.current_organization)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        role = Membership.objects.filter(user=self.request.user,
                                         organization=self.request.user.current_organization).first().role
        if role in ['owner', 'admin']:
            context['task'] = Task.objects.filter(id=self.kwargs['task_id'],
                                                  organization=self.request.user.current_organization,
                                                  is_active=True).first()
            if context['task'] is None:
                raise Http404('Tarefa nao encontrada')
        else:
            context['task'] = Task.objects.filter(id=self.kwargs['task_id'], user=self.request.user,
                                                  organization=self.request.user.current_organization,
                                                  is_active=True).first()
            if context['task'] is None:
                raise Http404('Tarefa nao encontrada')
        return context


class EditarTaskView(UpdateView):
    model = Task
    pk_url_kwarg = 'task_id'
    fields = ['completed']
    template_name = 'tasks/task_edit.html'

    def get_queryset(self):
        return Task.objects.filter(id=self.kwargs['task_id'], organization=self.request.user.current_organization,
                                   is_active=True)

    def get_object(self, queryset=None):

        if queryset is None:
            queryset = self.get_queryset()
            obj = queryset.first()
            print(obj)
        if obj is None:
            raise PermissionError('Tarefa nao encontrada')
        return obj

    def form_valid(self, form):
        task = form.save(commit=False)
        task.save()
        return redirect('mostrar_tarefas')


class DeleteTaskView(DeleteView):
    model = Task
    pk_url_kwarg = 'task_id'
    fields = ['deleted']
    template_name = 'tasks/task_delete.html'

    def dispatch(self, request, *args, **kwargs):
        user_membership = Membership.objects.filter(user=self.request.user,
                                                    organization=self.request.user.current_organization).first()
        if not user_membership or user_membership.role not in ['admin', 'owner']:
            return redirect('unauthorized')
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return Task.objects.filter(id=self.kwargs['task_id'], organization=self.request.user.current_organization,
                                   is_active=True)

    def get_object(self, queryset=None):
        if queryset == None:
            queryset = self.get_queryset()
            obj = queryset.first()
        if obj is None:
            raise Http404('Tarefa nao encontrada')
        return obj

    def post(self, request, *args, **kwargs):
        if self.request.POST:
            task = self.get_object()
            print(task)
            if task:
                user_membership = Membership.objects.filter(user=self.request.user,
                                                            organization=self.request.user.current_organization).first()
                if user_membership.role in ['admin', 'owner']:
                    task.is_active = False
                    task.save()
                    return redirect('mostrar_tarefas')
                else:
                    raise PermissionError("Voce não pode apagar essa tarefa")
            else:
                return redirect('erro404')

        return redirect('mostrar_tarefas')


class CategoryCreateView(CreateView):
    model = Category
    fields = ['title', 'description']
    template_name = 'tasks/category_create.html'

    def dispatch(self, request, *args, **kwargs):
        user_membership = Membership.objects.filter(user=self.request.user,
                                                    organization=self.request.user.current_organization).first()
        if not user_membership or user_membership.role not in ['admin', 'owner']:
            return redirect('unauthorized')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        category = form.save(commit=False)
        category.organization = self.request.user.current_organization
        category.save()
        return redirect('mostrar_tarefas')
