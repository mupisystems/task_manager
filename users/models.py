from django.db import models
from django.contrib.auth.models import User
from django.db.models import CASCADE


class Organization(models.Model):
    name = models.CharField(max_length=30)
    owner = models.ForeignKey(User, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    name = models.CharField(max_length=30)
    def __str__(self):
        return self.name
