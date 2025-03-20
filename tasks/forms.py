from django import forms
from django.contrib.auth import get_user_model
from .models import Category, Task, Comment

User = get_user_model()

class CreateCategory(forms.ModelForm):

    class Meta:
        model = Category
        
        fields = ['name']

        labels = {
            'name' : 'Nome do Categoria',
        }
    
    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super(CreateCategory, self).__init__(*args, **kwargs)

    def clean_name(self):
        name = self.cleaned_data['name']
        if not name:
            raise forms.ValidationError("O nome da categoria não pode estar vazio.")
        if Category.objects.filter(name=name, organization=self.organization).exists():
            raise forms.ValidationError("Essa categoria já existe na sua organização.")
        return name

class CreateTask(forms.ModelForm):

    class Meta:
        model = Task
        fields = ['title', 'description', 'due_date', 'category']

        labels = {
            'title' : 'Titulo da tarefa',
            'description' : 'Descrição da tarefa',
            'due_date' : 'Prazo',
        }

    due_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'})
    )
    
    def __init__(self, *args, **kwargs):
        self.org_active = kwargs.pop('org_active', None)
        super(CreateTask, self).__init__(*args, **kwargs)

        if self.org_active:
            self.fields['category'].queryset = Category.objects.filter(
                organization=self.org_active,
                visible=True
            )
        else:
            self.fields['category'].queryset = Category.objects.none()  

class CreateTaskForOthers(CreateTask):
    class Meta(CreateTask.Meta):
        fields = CreateTask.Meta.fields + ['responsible']
        labels = {
            **CreateTask.Meta.labels,
            'responsible': 'Responsável',
        }

    def __init__(self, *args, **kwargs):
        org_active = kwargs.get('org_active')
        super().__init__(*args, **kwargs)

        if self.org_active:
            self.fields['responsible'] = forms.ModelChoiceField(
                queryset=User.objects.filter(org_active=self.org_active),
                label='Responsável',
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'})
            )
        else:
            self.fields['responsible'] = forms.ModelChoiceField(
                queryset=User.objects.none(),
                label='Responsável',
                required=True
            )
        
class CreateComment(forms.ModelForm):

    class Meta:
        model = Comment
        #  create_by - pegar pela view
        # task - pegar pela view
        fields = ['text']

        labels = {
            'text' : 'Comentario',
        }
