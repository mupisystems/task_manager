from django import forms
from allauth.account.forms import SignupForm
from .models import CustomUser, Organization, Membership

class CustomSignupForm(SignupForm):
    name_user = forms.CharField(max_length=100, label='Nome', required=True)
    name_org = forms.CharField(max_length=100, label='Nome da Organização', required=True)
    
    def save(self, request):
        user = super().save(request)
        user.name_user = self.cleaned_data['name_user']
        user.org_active = Organization.objects.create(name_org=self.cleaned_data['name_org']) # (name=name_org)
        user.save()

        Membership.objects.create(user=user, organization=user.org_active, role='owner')
        return user

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs['placeholder'] = 'exemplo@email.com'
        
        self.fields['password1'].label = 'Senha'
        self.fields['password1'].widget.attrs['placeholder'] = 'Crie uma senha segura'
        
        self.fields['password2'].label = 'Confirmar Senha'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repita a senha'
        
        self.fields['name_user'].widget.attrs['placeholder'] = 'Digite seu nome completo'
        self.fields['name_org'].widget.attrs['placeholder'] = 'Nome da equipe ou organização'

class Userform(forms.ModelForm):
    class Meta:
        model = CustomUser
        
        fields = ['name_user','email']

        labels = {
            'name_user' : 'Nome do Membro',
            'email': 'Email',
            # 'password': 'Digite uma Senha',
        }
    