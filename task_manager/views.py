from django.shortcuts import render
from django.template.context_processors import request
from django.views.generic import TemplateView, GenericViewError
# Create your views here.
class HomeView(TemplateView):
    template_name = 'home.html'

def error404(request):
    return render(request,'error404.html')