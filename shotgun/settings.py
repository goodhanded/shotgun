"""
Django settings for shotgun project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

import os

PROJECT_ROOT = os.path.dirname(__file__)

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
        'NAME': os.path.join(PROJECT_ROOT, 'db.sqlite3'),
    }
}

PUBLIC_ROOT = os.path.join(PROJECT_ROOT, 'public')
RESOURCES_ROOT = os.path.join(PROJECT_ROOT, 'resources')
STATIC_ROOT = os.path.join(PUBLIC_ROOT, 'static')
MEDIA_ROOT = os.path.join(PUBLIC_ROOT, 'uploads')

STATIC_URL = '/static/'
MEDIA_URL = '/uploads/'

STATICFILES_DIRS = (
    os.path.join(PUBLIC_ROOT, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(RESOURCES_ROOT, 'templates'),
)
