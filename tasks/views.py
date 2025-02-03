from django.http import HttpResponse
from django.contrib.auth.models import User
from tasks.models import Task
from django.shortcuts import render
from django.shortcuts import get_object_or_404



def TaskListView(request):
    tasks = Task.objects.all()
    return render(request, 'index.html', {'tasks': tasks})

def TaskDetailView(request, pk):
    task = Task.objects.get(pk=pk)
    return render(request, 'detail.html', {'task': task})

def TaskCreateView(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        finished_at = request.POST.get('finished_at')
        Task.objects.create(title=title, description=description, category=category, finished_at=finished_at,user=request.user)
        return HttpResponse('Tarefa criada com sucesso')
    else:
        return render(request, 'create.html')
    
def TaskUpdateView(request, pk):
    
    task = Task.objects.get(pk=pk)
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        category = request.POST.get('category')
        finished_at = request.POST.get('finished_at')
        task.title = title
        task.description = description
        task.category = category
        task.finished_at = finished_at
        task.save()
        return HttpResponse('Tarefa atualizada com sucesso')
    else:
        return render(request, 'update.html', {'task': task})
    
def TaskDeleteView(request, pk):
    task = get_object_or_404(Task, pk=pk)
    task.delete()
    return HttpResponse('Tarefa deletada com sucesso')