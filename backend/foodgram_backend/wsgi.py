import os

from django.core.wsgi import get_wsgi_application
from dotenv import load_dotenv

load_dotenv()

os.environ.setdefault(
    'DJANGO_SETTINGS_MODULE',
    f"foodgram_backend.settings.settings_{os.getenv('ENV', 'production')}",
),

application = get_wsgi_application()
