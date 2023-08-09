from .base import *
from os import environ

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'postgres',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'pg_db',
        'PORT': 5432,
    }
}

# SMTP config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'testing.brainstorm'
EMAIL_HOST = environ.get('EMAIL_HOST')
EMAIL_PORT = environ.get('EMAIL_PORT')
EMAIL_HOST_USER = environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = environ.get('EMAIL_USE_TLS')
