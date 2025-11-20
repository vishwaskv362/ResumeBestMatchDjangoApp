"""
URL configuration for AI Resume Hunter project.
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.matcher.api.urls')),
]
