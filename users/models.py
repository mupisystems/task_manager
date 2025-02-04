from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    class Meta:
        db_table = 'auth_user'

    email = models.EmailField(unique=True)
    is_active = models.BooleanField(default=True)
    full_name = models.CharField(max_length=255)
    organization = models.ForeignKey('Organization', on_delete=models.CASCADE, null=True, blank=True, related_name="profile")
    

    def __str__(self):
        
        
        return self.email


class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True)
    owner = models.OneToOneField(UserProfile, on_delete=models.CASCADE, related_name="owned_organization")
    members = models.ManyToManyField(UserProfile, related_name="organizations")

    def __str__(self):
        return self.name

