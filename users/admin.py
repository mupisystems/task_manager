from django.contrib import admin
from .models import Organization, UserProfile, User, Membership

admin.site.register(Organization)
admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Membership)
# Register your models here.
