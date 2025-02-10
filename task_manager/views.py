from django.views.generic import TemplateView, ListView, CreateView, UpdateView, DeleteView, DetailView

# Create your views here.
class HomeView(TemplateView):
    template_name = 'members.html'

    