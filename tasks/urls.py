from django.urls import path
from django.contrib.auth.decorators import login_required
from . import views

app_name = 'tasks'

urlpatterns = [
    path('category/', login_required(views.CategoryListView.as_view()), name='category'),
    path('category/create', login_required(views.CategoryCreateView.as_view()), name='create_category'),
    path('category/<int:pk>/edit/', login_required(views.CategoryUpdateView.as_view()), name='update_category'),
    path('category/<int:pk>/delete/', login_required(views.CategoryDeleteView.as_view()), name='delete_category'),


    path('tasks/', login_required(views.TaskListViewTEMP.as_view()), name='tasks'),
    path('tasks/create', login_required(views.TaskCreateView.as_view()), name='create_tasks'),
    path('tasks/<int:pk>/delete/', login_required(views.TaskDeleteView.as_view()), name='delete_tasks'),

    path('tasks_others/', login_required(views.TaskForOthersListView.as_view()), name='tasks_others'),
    path('tasks_others/create', login_required(views.TaskCreateForOthersView.as_view()), name='create_tasks_others'),
]