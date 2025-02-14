from django.db import models
from teams.models import Team, Membership, User

class Task(models.Model):
    CHOICE_STATUS = [
        ('todo', 'À fazer'),
        ('doing', 'Fazendo'),
        ('done', 'Feito'),
    ]

    
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    deadline = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    status = models.CharField(max_length=7, choices=CHOICE_STATUS, default='todo')
    team = models.ForeignKey(Team, on_delete=models.CASCADE, default='')
    member = models.ForeignKey(Membership, on_delete=models.DO_NOTHING, default='')
    categoria = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL, default='')
    
    def __str__(self):
        return f'{self.title}, {self.member}'


class Category(models.Model):
    category_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.category_name