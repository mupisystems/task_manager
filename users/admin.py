from django.contrib import admin
from .models import Organization,UserProfile,MemberShip
from django.contrib.auth.models import User

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner',)

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(UserProfile)
admin.site.register(MemberShip)
