from django.template.context_processors import request
from .models import User
from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.shortcuts import redirect



class ChangePasswordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response


    def __call__(self, request):
        if request.user.is_authenticated:
            user = request.user
            if user.first_login:
                if request.path == '/accounts/password/change/' and request.method == 'POST':
                    user.first_login = False
                    user.save()
                else:
                    if request.path != '/accounts/password/change/':
                         return redirect('account_change_password')
        return self.get_response(request)





