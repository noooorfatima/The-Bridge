"""
WSGI config for new_bridge project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

"""
OLD - DJANGO 1.6
import os
import sys
sys.path.append('/opt/new_bridge/')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "new_bridge.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
"""

# new for Django 1.7
import os
import sys

from django.core.wsgi import get_wsgi_application

os.environ['DJANGO_SETTINGS_MODULE'] = 'new_bridge.settings'
application = get_wsgi_application()
