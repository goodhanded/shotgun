"""
Django settings for shotgun project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['uncviscom.webfactional.com','shotgun.uncviscom.webfactional.com']


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'uncviscom_shotgun',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'uncviscom_shotgun',
        'PASSWORD': 'Pri-31e-Tru-Squ',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
    }
}


# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = '/home/uncviscom/webapps/static_media/'

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = 'http://uncviscom.webfactional.com/static/'

# EMAIL_HOST = 'smtp.webfaction.com'
# EMAIL_HOST_USER = 'mailbox_username'
# EMAIL_HOST_PASSWORD = 'mailbox_password'
# DEFAULT_FROM_EMAIL = 'valid_email_address'
# SERVER_EMAIL = 'valid_email_address'
