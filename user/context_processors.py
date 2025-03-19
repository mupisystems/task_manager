from .models import Membership  # use o caminho correto

def role_user_org_ativa(request):
    cargo = None
    if request.user.is_authenticated and request.user.org_active:
        try:
            membership = Membership.objects.get(
                organization=request.user.org_active,
                user=request.user,
                is_active=True
            )
            cargo = membership.role  # 'owner', 'admin', 'member'
        except Membership.DoesNotExist:
            cargo = None
    return {'role_user': cargo}
