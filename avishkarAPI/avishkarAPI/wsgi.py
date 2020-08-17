"""
WSGI config for avishkarAPI project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/howto/deployment/wsgi/
"""

import os
import sys

sys.path.append('/home/sahaj/Projects/Django/avishkarAPI')
sys.path.append('/home/sahaj/Projects/Django/avishkarAPI/avishkar/lib/python3.6/site-packages')



from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avishkarAPI.settings')

application = get_wsgi_application()
