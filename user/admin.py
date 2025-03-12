from django.contrib import admin
from .models import CustomUser, Organization, Membership

# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Organization)
admin.site.register(Membership)