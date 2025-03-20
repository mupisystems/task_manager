from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import CategoryListView, CategoryCreateView, TaskListViewTEMP, TaskCreateView, TaskForOthersListView, TaskCreateForOthersView

app_name = 'tasks'

urlpatterns = [
    path('category/', login_required(CategoryListView.as_view()), name='category'),
    path('category/create', login_required(CategoryCreateView.as_view()), name='create_category'),

    path('tasks/', login_required(TaskListViewTEMP.as_view()), name='tasks'),
    path('tasks/create', login_required(TaskCreateView.as_view()), name='create_tasks'),

    path('tasks_others/', login_required(TaskForOthersListView.as_view()), name='tasks_others'),
    path('tasks_others/create', login_required(TaskCreateForOthersView.as_view()), name='create_tasks_others'),
]