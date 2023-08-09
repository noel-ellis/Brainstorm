from .base import *
from environ import Env

env = Env()
env.read_env(env.str('../../', '.env'))

ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DB_NAME'),
        'USER': env.str('DB_USER'),
        'PASSWORD': env.str('DB_PASSWORD'),
        'HOST': 'localhost',
        'PORT': 5432,
    }
}

# SMTP config
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
DEFAULT_FROM_EMAIL = 'testing.brainstorm'
EMAIL_HOST = env.str('EMAIL_HOST')
EMAIL_PORT = env.str('EMAIL_PORT')
EMAIL_HOST_USER = env.str('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = env.str('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = env.str('EMAIL_USE_TLS')
