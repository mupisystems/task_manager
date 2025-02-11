from django import forms
from allauth.account.forms import SignupForm,LoginForm
from django.contrib.auth import get_user_model
from .models import Organization, MemberShip

class CustomLoginForm(LoginForm):



    field_order = ['login', 'password']

    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['login'].label = 'Email'
        self.fields['password'].label = 'Senha'

    
    

User = get_user_model() 

class CustomSignupForm(SignupForm):
    organization_name = forms.CharField(
        max_length=255, 
        required=True, 
        label="Nome da Organização:"
    )
    full_name = forms.CharField(
        max_length=255, 
        required=True, 
        label="Nome completo:"
    )

    
    field_order = ['organization_name','full_name', 'email', 'password1', 'password2']

    email = forms.EmailField(
        max_length=254, 
        required=True, 
        label="Email:"
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].widget.attrs['autofocus'] = True
        self.fields['email'].widget.attrs['placeholder'] = 'Digite seu email'
        self.fields['full_name'].widget.attrs['placeholder'] = 'Digite seu nome completo'
        self.fields['organization_name'].widget.attrs['placeholder'] = 'Nome da sua organização'


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ja cadastrado. Escolha outro")
        return email
    
    def clean_organization_name(self):
        organization_name = self.cleaned_data['organization_name']
        if Organization.objects.filter(name=organization_name).exists():
            raise forms.ValidationError("Organização ja cadastrada. Escolha outra")
        return organization_name
        



    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data['full_name']
        user.email = self.cleaned_data['email']
        org = Organization.objects.create(name=self.cleaned_data['organization_name'],owner=user)
        user.organization = org
        MemberShip.objects.create(user=user, organization=org, role='master')
        user.save()
        return user


class RegisterNewMemberForm(SignupForm):

    print(MemberShip.roles)
    role = forms.ChoiceField(
        choices=[('member', 'Membro'), ('admin', 'Admin')],
        widget=forms.RadioSelect,
        label='Cargo'
    )

    email = forms.EmailField(
        max_length=254,
        required=True,
        label="Email:",
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'placeholder': 'Email do novo usuário'
        })
    )

    field_order = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado.")
        return email

    def save(self, request):
        user = super().save(request)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        return user 
    
