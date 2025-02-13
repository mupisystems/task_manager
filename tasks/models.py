from django.db import models
from users.models import UserProfile,MemberShip,Organization



class Task(models.Model):

    choices = [
        ('TODO', 'TODO'),
        ('DONE', 'DONE'),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.BooleanField(default=False)
    due_date = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_assigned')
    created_by = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, related_name='user_created')

    def __str__(self):
        return self.title
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        
        return self.name
    

class Comment(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="comments")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.content