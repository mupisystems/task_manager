from django import forms
from .models import Task, Category, Comment
from users.models import UserProfile
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'status', 'category', 'assigned_to', 'due_date']
        
        widgets = {
            'due_date':forms.DateTimeInput(attrs={'type': 'datetime-local'},format='%Y-%m-%dT%H:%M')
        }

        labels = {
            'title': 'Título',
            'description': 'Descrição',
            'assigned_to': 'Atribuir a',
            'status':'Concluída',
            'category': 'Categoria',
            'due_date': 'Data de Vencimento'
        }   

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Remove o argumento 'user' antes de chamar o super

        super(TaskForm, self).__init__(*args, **kwargs)  # Evita o erro

        if user:
            org = user.organization
            self.fields['assigned_to'].queryset = UserProfile.objects.filter(
                organization=org, is_active=True
                ).distinct()         
            self.fields['category'].queryset = Category.objects.filter(
                created_by=org
                ).distinct()    


    def clean_title(self):
            title = self.cleaned_data['title']
            if not title:
                raise forms.ValidationError("Título obrigatório")
            return title
        
    def clean_description(self):
            description = self.cleaned_data['description']
            if len(description) < 10:
                raise forms.ValidationError("A descrição deve ter pelo menos 10 caracteres")
            return description

    def clean_assigned_to(self):
            assigned_to = self.cleaned_data['assigned_to']
            if not assigned_to:
                raise forms.ValidationError("Você deve atribuir a tarefa para um usuário")
            return assigned_to
        
    def clean_category(self):
            category = self.cleaned_data['category']
            if not category:
                raise forms.ValidationError(" Vocé deve escolher uma categoria")
            return category
        
    def save(self, commit=True):
        task = super().save(commit=False)

            # Associar o usuário autenticado ao campo 'created_by' (caso esteja implementado no seu modelo Task)
        if hasattr(self, 'request'):
                task.created_by = self.request.user
                task.assigned_to = self.cleaned_data['assigned_to']

        if commit:
            task.save()

        return task

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
        labels = {'name': 'Nome da categoria'}
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome da categoria'}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)  # Pegamos o usuário, se fornecido
        super().__init__(*args, **kwargs)

    def clean_name(self):
        """Evita duplicatas dentro da mesma organização"""
        name = self.cleaned_data.get('name')
        if self.user and hasattr(self.user, 'organization'):
            org = self.user.organization
            if Category.objects.filter(name=name, created_by=org).exists():
                raise forms.ValidationError("Essa categoria já existe na sua organização.")
        return name

    def save(self, commit=True):
        """Salva a categoria com a organização do usuário"""
        Category = super().save(commit=False)
        if self.user and hasattr(self.user, 'organization'):
            Category.created_by = self.user.organization
        if commit:
            Category.save()
        return Category





class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']

    labels = {
        'content': 'Comentario'
    }