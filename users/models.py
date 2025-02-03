from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    age = models.IntegerField(default=0)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.user.username


class Organization(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name