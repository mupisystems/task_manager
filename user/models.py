from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    username = None 
    email = models.EmailField(unique=True)  
    name_user = models.CharField(max_length=100, unique=False)
    org_active = models.ForeignKey('Organization', on_delete=models.SET_NULL, null=True, blank=True, related_name="org_active")  
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'  
    REQUIRED_FIELDS = ['name_user']

    def __str__(self):
        return f"{self.name_user}  /  {self.email}"
    
class Organization(models.Model):
    name_org = models.CharField(max_length=100, unique=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        is_active = 'ativa' if self.is_active else 'desativada'
        return f"{self.name_org}  /  {is_active}"

    def get_active_members(self):
        return Membership.objects.filter(organization=self, is_active=True) 

class Membership(models.Model):

    class Role(models.TextChoices):
        OWNER = "owner", "dono" #colocar com boolean, só tem 1 por org
        ADMIN = "admin", "administrador"
        MEMBER = "member", "membro"
    role = models.CharField(max_length=20, choices=Role.choices, default= Role.MEMBER)

    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="members")
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="memberships")
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.organization.name_org} / {self.user.name_user} ({self.get_role_display()}) - {'Ativo' if self.is_active else 'Inativo'}"
    
