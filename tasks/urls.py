from django.urls import include, path
from tasks import views

urlpatterns = [
    path('taskCreate', views.TaskCreateView, name='taskCreate'),

]