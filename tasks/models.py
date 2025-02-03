from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):

    name = models.CharField(max_length=20)

    def __str__(self):

        return self.name


class Task(models.Model):

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=50, help_text="Título da sua tarefa")
    description = models.CharField(max_length=500, help_text="Descrição da sua tarefa")
    creation_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.BooleanField(default=False)
    category = models.CharField(max_length=20,help_text="Defina uma categoria")


    def __str__(self):

        return self.title 
    

class Comment(models.Model):

    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    comment = models.CharField(max_length=500)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment