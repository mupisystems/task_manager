from django.core.exceptions import PermissionDenied
from functools import wraps

def require_admin_or_owner(view_func):
    """
    Decorador para restringir acesso a usuários com cargo ADMIN ou OWNER na organização ativa.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Verifica se o usuário está autenticado
        if not request.user.is_authenticated:
            raise PermissionDenied("Você precisa estar autenticado para acessar esta página.")

        # Obtém a organização ativa do usuário
        org_active = request.user.org_active
        if not org_active:
            raise PermissionDenied("Você não está associado a uma organização ativa.")

        # Verifica o cargo do usuário na organização ativa
        membership = request.user.memberships.filter(organization=org_active, is_active=True).first()
        if not membership or membership.role == "member":
            raise PermissionDenied("Você não tem permissão para acessar esta página.")

        return view_func(request, *args, **kwargs)

    return _wrapped_view
