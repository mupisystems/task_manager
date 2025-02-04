from django.contrib import admin
from .models import Organization,UserProfile
from django.contrib.auth.models import User

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'get_members_count')
    
    def get_members_count(self, obj):
        return obj.members.count() 
    get_members_count.short_description = 'Membros' 

admin.site.register(Organization, OrganizationAdmin)
admin.site.register(UserProfile)
