"""This is a django-split-settings main file."""

from os import environ
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include, optional

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent

load_dotenv(dotenv_path=BASE_DIR.joinpath('movies_admin/config/.env'))


# Managing environment via `DJANGO_ENV` variable:
# To change settings file:
# `DJANGO_ENV=production python manage.py runserver`
environ.setdefault('DJANGO_ENV', 'development')
_ENV = environ['DJANGO_ENV']

_base_settings = (
    'components/common.py',
    'components/database.py',
    # Выбор настроек environment:
    'environments/{0}.py'.format(_ENV),
    # Опционально перезапись отдельных настроек:
    optional('environments/local.py'),
)

# Include settings:
include(*_base_settings)
