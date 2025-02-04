from django.http import HttpResponseRedirect
from django.shortcuts import render
from tasks.forms import TaskForm
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required


@login_required()
def TaskCreateView(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('home'))

    context = {'form': form}

    return render(request, 'tasks/task_form.html', context)


@login_required()
def TaskList(request):

    tasks = Task.objects.filter(organization=request.user.profile.current_organization)
    context = {'tasks': tasks}
    return render(request, 'tasks/task_list.html', context)


@login_required()
def MostrarTask(request, task_id):
    task = get_object_or_404(Task, id=task_id, organization=request.user.profile.current_organization)
    context = {'task': task}
    return render(request, 'tasks/task.html', context)


@login_required()
def EditarTask(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id, user=request.user, organization=request.user.profile.current_organization)
    except Http404:
        return HttpResponseRedirect(reverse('Erro404'))

    if request.method != 'POST':
        form = TaskForm(instance=task)

    else:
        form = TaskForm(instance=task, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('mostrarTask', args=[task.id]))

    context = {'form': form, 'task': task}

    return render(request, 'tasks/task_edit.html', context)

@login_required()
def deleteTask(request, task_id):
    try:
        task = get_object_or_404(Task, id=task_id)
    except Http404:
        return HttpResponseRedirect(reverse('Erro404'))
    task.delete()
    messages.success(request, "Tarefa deletada com sucesso!")
    return HttpResponseRedirect(reverse('taskList'))

@login_required()
def confirmDeleteTask(request, task_id):
    try:
     task = get_object_or_404(Task, id=task_id, user=request.user)
    except Http404:
        return HttpResponseRedirect(reverse('erro404'))

    if request.user.profile.role != 'owner':
        return HttpResponseRedirect(reverse('unauthorized'))

    context={'task': task}
    return render(request, 'tasks/task_delete.html', context)