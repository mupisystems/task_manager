from django import forms
from .models import Organization, Membership
from allauth.account.forms import SignupForm, LoginForm


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

        organization = Organization.objects.create(name=f'Equipe de {user.username}', created_by=user)
        Membership.objects.create(user=user, organization=organization, role='owner')

        user.save()

        return user


class FormLogin(LoginForm):

    def login(self, *args, **kwargs):

        return super(FormLogin, self).login(*args, **kwargs)
