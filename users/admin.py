from django.contrib import admin
from tasks.models import Task, Category, Comment
from users.models import UserProfile, MemberShip, Organization

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'category', 'created_at', 'assigned_to', 'created_by')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'description')

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at', 'created_by')
    search_fields = ('name',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('task', 'author', 'created_at')
    search_fields = ('content',)

@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'is_active')
    search_fields = ('name',)
    list_filter = ('is_active',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_active', 'organization')
    search_fields = ('username', 'email')
    list_filter = ('is_active', 'organization')

@admin.register(MemberShip)
class MemberShipAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'role', 'is_active')
    list_filter = ('role', 'is_active', 'organization')
    search_fields = ('user__username', 'organization__name')
