from django.urls import include, path
from tasks import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('taskCreate', login_required(views.TaskCreateView.as_view()), name='criar_tarefa'),
    path('taskList', login_required(views.TaskListView.as_view()), name='mostrar_tarefas'),
    path('mostrar-task/<task_id>', login_required(views.MostrarTaskView.as_view()), name='mostrar_task'),
    path('edit-task/<task_id>', login_required(views.EditarTaskView.as_view()), name='edit_task'),
    path('delete-task/<task_id>', login_required(views.DeleteTaskView.as_view()), name='delete_task'),
    path('create-category', login_required(views.CategoryCreateView.as_view()), name='criar_categoria'),

]