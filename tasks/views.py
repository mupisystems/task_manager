from django.http import HttpResponse
from django.contrib.auth.models import User
from tasks.models import Task
from django.shortcuts import render



def TaskListView(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

def TaskDetailView(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'detail.html', {'task': task})