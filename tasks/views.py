from django.http import HttpResponseRedirect
from django.shortcuts import render
from tasks.forms import TaskForm
from django.urls import reverse
from django.http import Http404
from django.shortcuts import get_object_or_404
from .models import Task
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def TaskCreateView(request):
    if request.method != 'POST':
        form = TaskForm()
    else:
        form = TaskForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            form.save()
            return HttpResponseRedirect(reverse('tasks'))

    context = {'form': form}

    return render(request, 'tasks/TaskCreate.html', context)
