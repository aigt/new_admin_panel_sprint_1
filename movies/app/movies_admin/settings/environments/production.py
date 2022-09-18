"""Файл содержит настройки для продакшена."""

import os

DEBUG = False


ALLOWED_HOSTS = [
    # TODO: check production hosts
    os.environ.get('DOMAIN_NAME'),
    # We need this value for `healthcheck` to work:
    '0.0.0.0',
]
