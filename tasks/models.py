from django.db import models
from user.models import Organization, CustomUser 

class Category(models.Model):
  name = models.CharField(max_length=50, null=True, blank=False)
  organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="organization")
  visible = models.BooleanField(default=True)

  class Meta:
    constraints = [
      models.UniqueConstraint(fields=['name', 'organization'], name='unique_category_per_org')
    ]

  def __str__(self):
    return f"{self.name}"

class Task(models.Model):
  title = models.CharField(max_length=200)
  description = models.TextField()
  category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
  responsible = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="responsible", null=True, blank=True) 
  by_organization = models.ForeignKey(Organization, on_delete=models.CASCADE, related_name="by_organization", null=True, blank=True)
  created_at = models.DateTimeField(auto_now_add=True)
  due_date = models.DateTimeField()
  completed = models.BooleanField(default=False) #Aqui se for completo
  visible = models.BooleanField(default=True) #Aqui se o usuário for removido (não mostra, mas não conclui)
  
  def __str__(self):
    return f"{self.id} / {self.title}"

class Comment(models.Model):
  create_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="create_by", null=True, blank=True)
  task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="task")
  text = models.TextField()
  visible = models.BooleanField(default=True)