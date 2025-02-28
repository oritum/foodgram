import os

from dotenv import load_dotenv

from . import settings_base
from .settings_base import ALLOWED_HOSTS

load_dotenv()

DEBUG = False

ALLOWED_HOSTS += os.getenv('ALLOWED_HOSTS', 'localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', 'django'),
        'USER': os.getenv('POSTGRES_USER', 'django'),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', ''),
        'HOST': os.getenv('DB_HOST', ''),
        'PORT': os.getenv('DB_PORT', 5432),
    }
}

MEDIA_ROOT = '/media/'

globals().update(
    {k: v for k, v in vars(settings_base).items() if not k.startswith("__")}
)
