from django import forms

from task_manager.settings import DEFAULT_PASSWORD
from .models import Organization, Membership
from allauth.account.forms import SignupForm, LoginForm, ChangePasswordForm


class FormRegistro(SignupForm):
    username = forms.CharField(
        max_length=15,
        required=True,
        label='Nome de Usuario')
    full_name = forms.CharField(
        max_length=60,
        required=True,
        label='Nome Completo'
    )

    # Modificando labels e help_texts dos campos padrão
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].label = "E-mail"
        self.fields['email'].help_text = "Informe um e-mail válido para cadastro."

        self.fields['password1'].label = "Senha"
        self.fields['password1'].help_text = "Sua senha deve ter pelo menos 8 caracteres."

        self.fields['password2'].label = "Confirme a senha"
        self.fields['password2'].help_text = "Repita a senha para confirmação."

    def save(self, request):
        user = super(FormRegistro, self).save(request)

        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.username = self.cleaned_data['username']
        user.first_login = False

        organization = Organization.objects.create(name=f'Equipe de {user.username}', created_by=user)
        Membership.objects.create(user=user, organization=organization, role='owner')

        user.save()

        return user


class FormLogin(LoginForm):

    def login(self, *args, **kwargs):
        return super(FormLogin, self).login(*args, **kwargs)


class CustomChangePasswordForm(ChangePasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['oldpassword'].label = "Senha Atual"

        self.fields['password1'].label = "Nova Senha"
        self.fields['password1'].help_text = (
            "Sua senha não pode ser muito semelhante às suas outras informações pessoais."
            "Sua senha deve conter pelo menos 8 caracteres."
            "Sua senha não pode ser uma senha comumente usada."
            "Sua senha não pode ser totalmente numérica.")

        self.fields['password2'].label = "Repita a Nova Senha"
        self.fields['password2'].help_text = "Repita a senha para confirmação."

    def save(self):
        super(CustomChangePasswordForm, self).save()
