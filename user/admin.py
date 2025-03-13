from django.contrib import admin
from .models import CustomUser, Organization, Membership

# Register your models here.

class CustomUserAdmin(admin.ModelAdmin):
  list_display = ("name_user", "email", "org_active", "is_active",)

  
admin.site.register(CustomUser, CustomUserAdmin)


class OrganizationAdmin(admin.ModelAdmin):
  list_display = ("name_org", "is_active", )

  
admin.site.register(Organization, OrganizationAdmin)

class MembershipAdmin(admin.ModelAdmin):
  list_display = ("organization", "user", "role", "is_active",)
  
admin.site.register(Membership, MembershipAdmin)


