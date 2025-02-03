from django.urls import include, path
from tasks import views

app_name = 'tasks'  

urlpatterns = [
    path('tasks',views.TaskListView,name='tasks'),
]