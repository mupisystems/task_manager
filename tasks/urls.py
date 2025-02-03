from django.urls import include, path
from .views import TaskListView, TaskCreateView, TaskDetailView, TaskUpdateView, TaskDeleteView

urlpatterns = [
    path('', TaskListView.as_view(), name="task-list"),
    path('task-details/<str:id>', TaskDetailView.as_view(), name="task-details"),
    path('task-create/', TaskCreateView.as_view(), name="task-create"),
    path('task-update/', TaskUpdateView.as_view(), name="task-update"),
    path('task-delete/', TaskDeleteView.as_view(), name="task-delete"),
]
