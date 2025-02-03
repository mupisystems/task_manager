from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=50, help_text="Título da sua tarefa" )
    description = models.CharField(max_length=500)
    creation_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.BooleanField(default=False)
    category = models.CharField(max_length=20)


    def __str__(self):

        return self.title 
    
