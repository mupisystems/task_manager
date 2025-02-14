from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model

class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    current_team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.email



class Team(models.Model):
    team_name = models.CharField(max_length=60, unique=True, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.team_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name
    


class Membership(models.Model):
    HIERARQUIA = [
        ("Proprietário", "Proprietário"),
        ("Administrador", "Administrador"),
        ("Colaborador", "Colaborador"),
    ]
    is_active = models.BooleanField(default=True)
    members = models.ForeignKey(User, blank=True, null=True, on_delete=models.DO_NOTHING, related_name='membership')
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    user_type = models.CharField(max_length=15, choices=HIERARQUIA, default="Colaborador")

    
    def __str__(self):
        return f'{self.team}, {self.members} cargo: {self.user_type}'
    
    def save(self, *args, **kwargs):
        if not self.pk:
            if not self.members and not self.members.current_team:
                self.members.current_team = self.team
                self.members.save()

        
        super(Membership, self).save(*args, **kwargs)
