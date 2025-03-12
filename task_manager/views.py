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
    
class OrgDetailView(DetailView):
    model = Organization
    template_name = 'details_org.html'
    context_object_name = 'organization'

    def get_object(self):
        organization_id = self.kwargs['pk']
        organization = get_object_or_404(Organization, id=organization_id)
        return organization

    