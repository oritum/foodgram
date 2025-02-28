import os

from . import settings_base
from .settings_base import BASE_DIR, INSTALLED_APPS, MIDDLEWARE

DEBUG = True

ALLOWED_HOSTS = [
    '127.0.0.1',
]

INSTALLED_APPS += ['debug_toolbar']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']

globals().update(
    {k: v for k, v in vars(settings_base).items() if not k.startswith("__")}
)
