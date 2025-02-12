from django import forms
from allauth.account.forms import SignupForm,LoginForm
from django.contrib.auth import get_user_model
from .models import Organization, MemberShip
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

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


class RegisterNewMemberForm(forms.Form):
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
    password1 = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput,
        required=True,
    )

    password2 = forms.CharField(
        label="Confirmação de Senha",
        widget=forms.PasswordInput,
        required=True,
    )

    field_order = ['email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        self.organization = kwargs.pop('organization', None)
        super().__init__(*args, **kwargs)

    def clean_email(self):
        email = self.cleaned_data.get('email').lower()
        if not email:
            raise ValidationError("O email é obrigatório.")
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        # Verifica se as senhas são iguais
        if password1 and password2 and password1 != password2:
            raise ValidationError("As senhas não coincidem.")

        # Valida a força da senha (opcional)
        if password1:
            validate_password(password1)

        return cleaned_data

    def get_or_create_user(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password1')
        user, created = User.objects.get_or_create(email=email)
        
        # Se o usuário já existir, apenas atualiza a organização (se necessário)
        if created:
            # Se o usuário for novo, define a senha com hash
            user.set_password(password)
            user.username = email  # Define o username como o email
            user.organization = self.organization  # Associa à organização
            user.save()
        else:
            # Se o usuário já existir, apenas atualiza a organização (se necessário)
            if not user.organization:
                user.organization = self.organization
                user.save()
        
        return user, created

    def save(self, commit=True):
        user, created = self.get_or_create_user()

        # Verifica se o usuário já é membro da organização
        if MemberShip.objects.filter(user=user, organization=self.organization).exists():
            raise ValidationError("Usuário já é membro desta equipe.")

        # Cria a associação (MemberShip) do usuário com a organização
        role = self.cleaned_data.get('role')
        membership = MemberShip(user=user, organization=self.organization, role=role)

        if commit:
            membership.save()

        return membership
