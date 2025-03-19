from django.contrib import admin
from .models import Category, Task, Comment

class CategoryAdmin(admin.ModelAdmin):
  list_display = ("name", "organization", )
admin.site.register(Category, CategoryAdmin)


class TaskAdmin(admin.ModelAdmin):
  list_display = ("title", "description", "category", "responsible", "by_organization", "created_at", "due_date", "completed", "visible", )
admin.site.register(Task, TaskAdmin)


class CommentAdmin(admin.ModelAdmin):
  list_display = ("task", "text", "create_by", "visible", )
admin.site.register(Comment, CommentAdmin)
