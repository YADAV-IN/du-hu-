import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "hello_world.settings")

from django.core.wsgi import get_wsgi_application

app = get_wsgi_application()
