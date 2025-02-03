from django import forms
from tasks.models import Task

class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ["title", "description", "completed", "due_date","category", "organization"]

        labels= {'title':'Titulo',
                 'description': 'Descrição',
                 'completed': 'Completa',
                 'due_date':'Prazo',
                 'category': 'Categoria',
                 'organization': 'Equipe'}

        widgets = {
            'due_date': DateInput()
        }