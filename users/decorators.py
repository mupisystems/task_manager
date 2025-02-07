from functools import wraps
from django.shortcuts import redirect
from users.models import Membership

def role_required(roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(self, request, *args, **kwargs):
            if not Membership.objects.filter(
                user=request.user,
                organization=request.user.current_organization,
                role__in=roles
            ).exists():
                return redirect('unauthorized')
            return view_func(self, request, *args, **kwargs)
        return _wrapped_view
    return decorator