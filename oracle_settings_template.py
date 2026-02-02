# Django Settings for Oracle Cloud Database Connection

# Add this to your hello_world/settings.py

import os
from pathlib import Path

# Oracle Database Configuration
DATABASES = {
    'default': {
        # Using oracledb (cx_Oracle alternative)
        'ENGINE': 'django.db.backends.oracle',
        
        # Connection Details (from Oracle Cloud)
        'NAME': os.environ.get('ORACLE_DB_NAME', 'duhubdb'),
        'USER': os.environ.get('ORACLE_DB_USER', 'admin'),
        'PASSWORD': os.environ.get('ORACLE_DB_PASSWORD', ''),
        'HOST': os.environ.get('ORACLE_DB_HOST', ''),
        'PORT': os.environ.get('ORACLE_DB_PORT', '1522'),
        
        # Additional Oracle settings
        'THREADED': True,  # Enable threading
        'USE_RETURNING_INTO': True,  # Use RETURNING INTO for inserts
        
        # Connection pooling (Optional but recommended)
        'CONN_MAX_AGE': 600,
        
        # Timeout settings
        'OPTIONS': {
            'threaded': True,
        },
    }
}

# Alternative: Using connection string
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.oracle',
#         'NAME': 'oracle://admin:password@hostname:1522/duhubdb',
#     }
# }

# Allowed Hosts
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1,duhubunofficial.local').split(',')

# DU HUB UNOFFICIAL Domain
SITE_NAME = 'DU HUB UNOFFICIAL'
DOMAIN_NAME = 'duhubunofficial.local'

# Debug Mode
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Secret Key
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-change-this-in-production')

# Static files configuration
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Security settings for production
SECURE_SSL_REDIRECT = not DEBUG
SESSION_COOKIE_SECURE = not DEBUG
CSRF_COOKIE_SECURE = not DEBUG
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    "default-src": ("'self'",),
}

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/tmp/django_errors.log',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'console'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
