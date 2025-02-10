from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True, related_name="profile")

    def __str__(self):
        
        return f"{self.username}"


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="owned_organization")

    def __str__(self):
        return f"{self.name}"


class MemberShip(models.Model):

    roles = [
        ('master', 'Master'),
        ('admin', 'Admin'),
        ('member', 'Member')    
    ]

    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="user_membership")
    role = models.CharField(max_length=255, choices=roles)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="org_membership")

    def __str__(self):
        return f"{self.user} - {self.organization}"