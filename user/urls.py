from django.urls import path
from .views import CreateUserView, MyOrgsListView, set_active_org, OrgDetailView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('creat_user/', CreateUserView.as_view(), name='creat_user'),
    path('my_orgs/', login_required(MyOrgsListView.as_view()), name='my_orgs'),
    path('set_active_org/<int:org_id>/', login_required(set_active_org), name='set_active_org'),
    
    path('members/', OrgDetailView.as_view(), name='members'),
]
