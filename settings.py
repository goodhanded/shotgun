"""
Django settings for shotgun project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

PROJECT_ROOT = os.path.dirname(__file__)
SITE_ROOT = os.path.dirname(PROJECT_ROOT)

SECRET_KEY = '8xsh%by4t5^tk+h$)0(hzl49f5jun2=a)hm*a!u^+3qvc7dqd%'

DEBUG = True
TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'America/New_York'

USE_I18N = True
USE_L10N = True
USE_TZ = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registration',
    'south',
    'drive',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.messages.context_processors.messages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

ROOT_URLCONF = 'shotgun.urls'
WSGI_APPLICATION = 'shotgun.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(SITE_ROOT, 'db.sqlite3'),
    }
}

RESOURCES_ROOT = os.path.join(PROJECT_ROOT, 'resources')
PUBLIC_ROOT = os.path.join(RESOURCES_ROOT, 'public')
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'static')
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'uploads')

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATICFILES_DIRS = (
    PUBLIC_ROOT,
)

TEMPLATE_DIRS = (
    os.path.join(RESOURCES_ROOT, 'templates'),
)

# Configure django-registration
ACCOUNT_ACTIVATION_DAYS = 7 # One-week activation window; you may, of course, use a different value.

# Configure email
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'shotgun.ride.share@gmail.com'
EMAIL_HOST_PASSWORD = 'simonerocks'
EMAIL_PORT = 587
EMAIL_USE_TLS = True