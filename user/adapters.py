from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

class CustomAccountAdapter(DefaultAccountAdapter):
    def send_mail(self, template_prefix, email, context):
        if template_prefix == "account/email/password_reset_key":
            print(f"Código de redefinição de senha para {email}: {context['password_reset_url']}")
        else:
            super().send_mail(template_prefix, email, context)