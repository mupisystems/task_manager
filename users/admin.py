from django.contrib import admin
from .models import Organization, UserProfile, User, Funcao

admin.site.register(Organization)
admin.site.register(UserProfile)
admin.site.register(User)
admin.site.register(Funcao)
# Register your models here.
