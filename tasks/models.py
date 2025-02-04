from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.db.models import CASCADE, DO_NOTHING, ManyToManyField
from users.models import Organization, User


class Category(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=False, default='')

    class Meta:
        verbose_name_plural = "Categories"


    def __str__(self):
        return self.title

class Task(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField(blank=True, null=False, default='')
    completed = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField()
    organization = models.ForeignKey(Organization, on_delete=CASCADE)
    user = models.ForeignKey(User, on_delete=DO_NOTHING)

    def __str__(self):
        return self.title


class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=CASCADE)
    content = models.TextField()
    task = models.ForeignKey(Task, on_delete=CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Comments"
    def __str__(self):
        return f"Comment by {self.user} on {self.task}"