from django import forms
from .models import Team, Membership
from django.core.exceptions import ValidationError
from allauth.account.forms import LoginForm, SignupForm


class MyCustomSignupForm(SignupForm):
    team_name = forms.CharField(label='Nome da organização', max_length=30, required=True)
    full_name = forms.CharField(label='Seu nome completo', max_length=100, required=True)

    field_order = ['team_name']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.fields['team_name'].widget.attrs['placeholder'] = 'Digite o nome da sua organização'
        self.fields['full_name'].widget.attrs['placeholder'] = 'Digite seu nome'
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu email'
        self.fields['password1'].help_text = ''
        self.fields['password1'].widget.attrs['placeholder'] = 'Digite uma senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Digite novamente sua senha'
        self.fields['password1'].label = 'Senha'
        self.fields['password2'].label = 'Repita sua senha'
        
        del self.fields['username']


    def clean_team_name(self):
        team_name = self.cleaned_data.get("team_name")
        if Team.objects.filter(team_name = team_name).exists():
            raise ValidationError('Já existe uma organização com esse nome')
        return team_name
    

    def save(self, request):
        user = super(MyCustomSignupForm, self).save(request)
        team_name = self.cleaned_data.get("team_name")
        team = Team.objects.create(team_name = team_name)
        full_name = self.cleaned_data.get('full_name')
        name_arr = full_name.split(" ", 1)
        first_name = name_arr[0]
        last_name = name_arr[1] if len(name_arr) > 1 else ""
        user.first_name = first_name
        user.last_name = last_name

        print(team)
        Membership.objects.create(team=team, members = user, user_type = 'Proprietário', is_active = True)
        user.save()
        return user
    


class MyCustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].widget.attrs['placeholder'] = 'Digite seu email'
        self.fields['password'].widget.attrs['placeholder'] = 'Digite sua senha'
        self.fields['remember'].label = 'Lembrar-me'
        self.fields['password'].label = 'Senha'