from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import TaskListView

app_name = 'tasks'

urlpatterns = [
    path('tasks/', login_required(TaskListView.as_view()), name='tasks'),
]