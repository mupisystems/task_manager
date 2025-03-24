from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'tasks'

urlpatterns = [
    path('category/', views.CategoryListView.as_view(), name='category'),
    path('category/create', views.CategoryCreateView.as_view(), name='create_category'),
    path('category/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='update_category'),
    path('category/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='delete_category'),

    path('tasks/', login_required(views.TaskListViewTEMP.as_view()), name='tasks'),
    path('tasks/create', login_required(views.TaskCreateView.as_view()), name='create_tasks'),
    path('tasks/<int:pk>/delete/', login_required(views.TaskDeleteView.as_view()), name='delete_tasks'),
    path('tasks/<int:pk>/complete/', login_required(views.CompleteTaskView.as_view()), name='complete_task'),
    path('tasks/<int:pk>/edit/', login_required(views.TaskEditView.as_view()), name='edit_task'),
    path('tasks/<int:pk>/', login_required(views.TaskDetailView.as_view()), name='task_detail'),

    path('tasks_others/', views.TaskForOthersListView.as_view(), name='tasks_others'),
    path('tasks_others/create', views.TaskCreateForOthersView.as_view(), name='create_tasks_others'),
]