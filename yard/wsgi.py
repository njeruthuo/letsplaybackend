"""
WSGI config for yard project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/wsgi/
"""

import os
from whitenoise import WhiteNoise
from .settings import BASE_DIR

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'yard.settings')

application = get_wsgi_application()
application = WhiteNoise(
    application, root=os.path.join(BASE_DIR, 'staticfiles'))
