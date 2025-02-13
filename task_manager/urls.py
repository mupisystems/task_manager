from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from debug_toolbar.toolbar import debug_toolbar_urls

urlpatterns = [
    path('tasks/', include('tasks.urls')),
    path('accounts/', include('allauth.urls')),
    path('teams/', include('teams.urls')),
    path('admin/', admin.site.urls),
]  

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('debug/', include(debug_toolbar.urls)),
    ] + urlpatterns
