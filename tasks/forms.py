from django import forms
from .models import Category, Task, Comment

class CreateCategory(forms.ModelForm):

    class Meta:
        model = Category
        
        fields = ['name']

        labels = {
            'name' : 'Nome do Categoria',
        }
    