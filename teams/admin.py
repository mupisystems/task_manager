from django.contrib import admin
from .models import User, Team, Membership

# Register your models here.
admin.site.register(User)
admin.site.register(Team)
admin.site.register(Membership)