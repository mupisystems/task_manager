from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DetailView
from .models import Team

class TeamListView(ListView):
    model = Team
    template_name = 'teams/show_teams.html'
    context_object_name = 'teams'

class TeamDetailView(DetailView):
    model = Team
    template_name = 'teams/team_details'

class TeamCreateView(CreateView):
    model = Team
    fields = ['team_name']
    