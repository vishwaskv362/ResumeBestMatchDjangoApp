"""
ASGI config for resume_matcher_django project.
"""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.base')

application = get_asgi_application()
