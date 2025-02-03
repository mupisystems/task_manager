from django.db import models

class Task(models.Model):
    CHOICE_STATUS = (
        ('1', 'À fazer'),
        ('2', 'Fazendo'),
        ('3', 'Feito'),
    )

    
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    status = models.CharField(max_length=1, choices=CHOICE_STATUS)

    def __str__(self):
        return self.title


