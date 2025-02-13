from django.urls import path
from . import views

urlpatterns = [
    path('', views.TaskListView.as_view(), name='task_list'),
    path('task/<int:pk>/', views.TaskDetailView.as_view(), name='task_details'),
    path('create-task/', views.TaskCreateView.as_view(), name='task_create'),
    # path('task/delete/', views.TaskDeleteView.as_view(), name='task_delete'),
    # path('task/delete/', views.TaskUpdateView.as_view(), name='task_update'),
]
                                        