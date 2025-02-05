from django.urls import include, path
from tasks import views

urlpatterns = [
    path('taskCreate', views.TaskCreateView, name='taskCreate'),
    path('taskList', views.TaskListView.as_view(), name='taskList'),
    path('mostrar_task/<task_id>', views.MostrarTask, name='mostrarTask'),
    path('edit_task/<task_id>', views.EditarTask, name='editTask'),
    path('delete_task/<task_id>', views.confirmDeleteTask, name='deleteTask'),
    path('delete/<task_id>', views.deleteTask, name='apagar')

]