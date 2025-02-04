from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
class Team(models.Model):
    HIERARQUIA = [
        ("Administrador", "Administrador"),
        ("Proprietário", "Proprietário"),
        ("Colaborador", "Colaborador"),
    ]
    
    team_name = models.CharField(max_length=60)
    owner = models.ForeignKey("teams.User", blank=False, default='USERNAME', on_delete=models.CASCADE, to_field='username')
    slug = models.SlugField(unique=True, blank=True)
    user_type = models.CharField(max_length=13, choices=HIERARQUIA, default="Colaborador")

    def save(self, *args, **kwargs):
        if not self.slug:  
            self.slug = slugify(self.team_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team_name