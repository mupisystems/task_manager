from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import TemplateView, View, ListView
# Create your views here.

class HomeView(TemplateView):
    template_name = 'home.html'

class Error404View(View):
    template_name = 'error404.html'

class Unauthorized(View):
    template_name = 'unauthorized.html'