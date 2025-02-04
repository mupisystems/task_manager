from django import forms
from .models import UserProfile
from allauth.account.forms import SignupForm

class UserProfileForm(SignupForm):

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'full_name']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if UserProfile.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está em uso. Escolha outro.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if UserProfile.objects.filter(username=username).exists():
            raise forms.ValidationError('Este username já está em uso. Escolha outro.')
        return username
    