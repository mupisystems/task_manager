from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, View
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Team, Membership, User
from allauth.account.views import LogoutView


class TeamListView(ListView):
    model = Team
    template_name = 'teams/index.html'
    context_object_name = 'teams'
    

class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_details.html'
    

class TeamDeleteView(DetailView):
    model = Team
    success_urls = reverse_lazy('team_list')