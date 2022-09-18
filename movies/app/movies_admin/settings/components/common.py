"""Django common settings for config project."""

import os

from movies_admin import settings

SECRET_KEY = os.environ.get('SECRET_KEY')


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'movies_admin.apps.movies.apps.MoviesConfig',
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


ROOT_URLCONF = 'movies_admin.urls'


WSGI_APPLICATION = 'movies_admin.wsgi.application'


# Password validation
_PASS = 'django.contrib.auth.password_validation'  # noqa: S105
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': '{0}.UserAttributeSimilarityValidator'.format(_PASS)},
    {'NAME': '{0}.MinimumLengthValidator'.format(_PASS)},
    {'NAME': '{0}.CommonPasswordValidator'.format(_PASS)},
    {'NAME': '{0}.NumericPasswordValidator'.format(_PASS)},
]


# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(settings.BASE_DIR, 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(settings.BASE_DIR, 'media/')
