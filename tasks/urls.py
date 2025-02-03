from django.urls import include, path
from tasks import views

app_name = 'tasks'  

urlpatterns = [
    path('list',views.TaskListView,name='tasks'),
    path('list',views.TaskListView,name='tasks'),
    path('create',views.TaskCreateView,name='create'),
    path('detail/<int:pk>',views.TaskDetailView,name='detail'),
    path('update/<int:pk>',views.TaskUpdateView,name='update'),
    path('delete/<int:pk>',views.TaskDeleteView,name='delete'),
]