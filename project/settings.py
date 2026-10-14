"""
Django settings for windwardapps.com.

One settings module for every environment. Anything that differs between
local and production comes from environment variables (or a .env file at the
repo root, which is loaded if present).

    DEBUG=1                 turn on debug mode (local only)
    WA_SECRET_KEY           required when DEBUG is off
    ALLOWED_HOSTS           comma separated; defaults to windwardapps.com
    STATIC_ROOT             where collectstatic writes; defaults to ./static
    WA_CONTACT_EMAIL        where contact-form messages are delivered
    WA_EMAIL_API_URL        Mailgun-style messages endpoint
    WA_EMAIL_API_KEY        API key for the endpoint above
    CAPTCHA_KEY             hCaptcha site key (public)
    CAPTCHA_SECRET          hCaptcha secret
    CAPTCHA_ENFORCE=1       reject contact submissions that fail the captcha
    WA_BAD_EMAILS           comma separated senders whose contact messages are dropped
"""

import os
from pathlib import Path

from django.core.exceptions import ImproperlyConfigured
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')


def env(name, default=''):
    return os.environ.get(name, default)


def env_bool(name, default=False):
    return env(name, '1' if default else '0').strip().lower() in ('1', 'true', 'yes', 'on')


def env_list(name, default):
    value = [item.strip() for item in env(name).split(',') if item.strip()]
    return value or default


# --- Core -------------------------------------------------------------------

DEBUG = env_bool('DEBUG')

SECRET_KEY = env('WA_SECRET_KEY') or ('dev-only-insecure-key' if DEBUG else '')
if not SECRET_KEY:
    raise ImproperlyConfigured('WA_SECRET_KEY must be set when DEBUG is off')

ALLOWED_HOSTS = env_list('ALLOWED_HOSTS', ['*'] if DEBUG else ['windwardapps.com', 'www.windwardapps.com'])
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS if host != '*']

if not DEBUG:
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True

INSTALLED_APPS = [
    'app',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'
WSGI_APPLICATION = 'project.wsgi.application'
APPEND_SLASH = False

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# --- Database ---------------------------------------------------------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Existing tables were created with 32-bit ids; keep new ones consistent.
DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

# Shared across gunicorn workers; backs the rate limiter on public forms.
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.filebased.FileBasedCache',
        'LOCATION': str(BASE_DIR / '.cache'),
    }
}

# --- Auth -------------------------------------------------------------------

LOGIN_URL = '/login'

# --- Internationalization ---------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# --- Static files -----------------------------------------------------------

STATIC_URL = '/static/'
STATIC_ROOT = env('STATIC_ROOT', str(BASE_DIR / 'static'))

# --- Logging ----------------------------------------------------------------
# Everything goes to stderr. Under systemd that lands in the journal:
#   journalctl -u windwardapps.com -f

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {
            'format': '[%(levelname)s][%(name)s] %(message)s',
        },
    },
    'handlers': {
        'console': {'class': 'logging.StreamHandler', 'formatter': 'standard'},
    },
    'root': {
        'handlers': ['console'],
        'level': 'DEBUG' if DEBUG else 'INFO',
    },
}

# --- Site-specific ----------------------------------------------------------

CONTACT_EMAIL = env('WA_CONTACT_EMAIL')
BAD_EMAILS = {e.strip().lower() for e in env('WA_BAD_EMAILS').split(',') if e.strip()}
EMAIL_API_URL = env('WA_EMAIL_API_URL')
EMAIL_API_KEY = env('WA_EMAIL_API_KEY')

CAPTCHA_KEY = env('CAPTCHA_KEY')
CAPTCHA_SECRET = env('CAPTCHA_SECRET')
CAPTCHA_ENFORCE = env_bool('CAPTCHA_ENFORCE')
