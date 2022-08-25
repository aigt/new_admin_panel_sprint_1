"""Главный файл распределённых настроек."""

from os import environ
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include, optional

# Директория приложения
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Загрузка настроек в окружение
load_dotenv(dotenv_path=BASE_DIR.joinpath('config/.env'))


# Управление средой исполнения через переменную окружения `DJANGO_ENV`:
# Чтобы запустить другую среду:
# `DJANGO_ENV=production python manage.py runserver`
environ.setdefault('DJANGO_ENV', 'development')


_ENV = environ['DJANGO_ENV']


# Список файлов по которым распределены настройки
_base_settings = (
    'components/common.py',
    'components/database.py',
    'components/templates.py',
    'components/internationalization.py',
    # Выбор настроек environment:
    'environments/{0}.py'.format(_ENV),
    # Опционально перезапись отдельных настроек:
    optional('environments/local.py'),
)


# Загрузка настроек
include(*_base_settings)
