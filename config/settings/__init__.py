"""
Settings module initialization.
Import the appropriate settings based on environment.
"""
import os

environment = os.getenv('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
else:
    from .base import *
