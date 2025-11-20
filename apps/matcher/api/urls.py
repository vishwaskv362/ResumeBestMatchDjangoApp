"""
URL configuration for the matcher API.
"""
from django.urls import path
from apps.matcher.api import views

app_name = 'matcher'

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('stats/', views.stats_view, name='stats'),
    path('match/', views.resume_match_view, name='resume-match'),
]
