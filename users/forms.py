from django import forms
from .models import Organization, User, UserProfile
from django.contrib.auth.forms import UserCreationForm

class RegistroUser(UserCreationForm):
    email = forms.EmailField(required=True, label='E-Mail', widget=forms.EmailInput())
    first_name = forms.CharField(required=True, label='Primeiro Nome', widget=forms.TextInput(attrs={'class':'form-control'}))
    last_name = forms.CharField(required=True, label='Sobrenome', widget=forms.TextInput(attrs={'class':'form-control'}))
    username = forms.CharField(
        required=True,
        label='Nome de Usuario',
        widget=forms.TextInput(attrs={'class':'form-control'}),
        help_text='')

    password1 = forms.CharField(
        required=True,
        label='Senha',
        help_text='',
        widget=forms.PasswordInput(attrs={'class':'form-control'})
    )

    password2 = forms.CharField(
        required=True,
        label='Confirmação de Senha',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
        widgets = {
        }

        labels = {'username': 'Nome de Usuario',
                  'email': 'E-Mail',
                  'first_name': 'Primeiro Nome',
                  'last_name': 'Sobrenome',
                  'password1': 'Senha',
                  'password2': 'Confirme a Senha'}

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Esse e-mail já está em uso.")
        return email