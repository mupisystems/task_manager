from urllib import request
from users.forms import User
from .models import MemberShip,UserProfile,Organization

# def check_is_admin(user):
    
#     org = MemberShip.objects.filter(user=user).first()
#     # membership = MemberShip.objects.filter(user=user,organization_id=organization_id).first()
    

#     if(org.role == 'master'):
#         return True
#     else:
#         return False