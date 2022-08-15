"""
Этот файл содержит настройки, предназначенные только для разработки.

ПРЕДУПРЕЖДЕНИЕ БЕЗОПАСНОСТИ: не запускать в продакшн!
"""

from movies_admin.settings.components.common import INSTALLED_APPS, MIDDLEWARE

DEBUG = True


ALLOWED_HOSTS = [
    'localhost',
    '0.0.0.0',  # noqa: S104
    '127.0.0.1',
    '[::1]',
]


INSTALLED_APPS += ['debug_toolbar']


MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware']


INTERNAL_IPS = [
    '127.0.0.1',
]
