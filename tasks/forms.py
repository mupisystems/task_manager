from django import forms
from django.contrib.auth import get_user_model
from teams.models import User, Team, Membership
from .models import Task


class TaskForm(forms.ModelForm):
    member = forms.ModelChoiceField(queryset=Membership.objects.none())
    class Meta:
        model = Task
        fields = ('title', 'description', 'deadline', 'categoria', 'member', 'team')
        widgets = {
            'deadline':forms.DateTimeInput(attrs={'type': 'datetime-local'})
        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        print(user.current_team)
        super().__init__(*args, **kwargs)

        self.fields['title'].label = 'Título'
        self.fields['title'].widget.attrs['placeholder'] = 'Digite o título da sua tarefa'
        self.fields['description'].label = 'Descrição'
        self.fields['description'].required = False
        self.fields['deadline'].label = 'Prazo'
        self.fields['member'].label = 'Responsável'
        self.fields['team'].initial = user.current_team
        self.fields['team'].widget = forms.HiddenInput()


        if user and user.current_team:
            team_now = user.current_team
            self.fields['member'].queryset = Membership.objects.filter(
                team=team_now,
                is_active=True
            ).distinct()
