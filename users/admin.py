from django.contrib import admin
from .models import Organization, User, Membership

admin.site.register(Organization)

admin.site.register(User)
admin.site.register(Membership)
# Register your models here.
