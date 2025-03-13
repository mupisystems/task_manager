from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from user.models import Membership, Organization

# Create your views here.
class MyOrgListView(ListView):
    model = Membership
    template_name = 'home.html'
    context_object_name = 'orgs'

    def get_queryset(self):
        return Membership.objects.filter(user=self.request.user, is_active=True)
    



    