import logging
import os
from pathlib import Path

from dotenv import load_dotenv

from db import models
from settings import writer_adapters

# Директория приложения
BASE_DIR = Path(__file__).resolve().parent.parent


# Загрузка настроек в окружение из файла,
# если окружение PROD_ENV не установлено в production
_ENV = os.environ['PROD_ENV']
if _ENV != 'production':
    load_dotenv(dotenv_path=BASE_DIR.joinpath('../env_files/.env.db'))

# Количество записей обрабатываемых за раз
ROWS_PER_READ = 100


DATABASES = {
    'pg': {
        'database': os.environ.get('POSTGRES_DB'),
        'user': os.environ.get('POSTGRES_USER'),
        'password': os.environ.get('POSTGRES_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),  # noqa: WPS432
    },
    'sqlite': {
        'db_path': './db.sqlite',
    },
}


TABLE_MAP = {
    'film_work': (
        models.FilmWork,
        (
            writer_adapters.adapt_timestamps,
            writer_adapters.adapt_film_work_file_path,
        ),
    ),
    'person': (
        models.Person,
        (writer_adapters.adapt_timestamps,),
    ),
    'genre': (
        models.Genre,
        (
            writer_adapters.adapt_timestamps,
            writer_adapters.adapt_genre_description,
        ),
    ),
    'person_film_work': (
        models.PersonFilmWork,
        (writer_adapters.adapt_timestamps,),
    ),
    'genre_film_work': (
        models.GenreFilmWork,
        (writer_adapters.adapt_timestamps,),
    ),
}

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'standard': {'format': '%(asctime)s %(levelname)s - %(name)s: %(message)s'},
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'formatter': 'standard',
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        '': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': False,
        },
    },
}


DB_DDL_SCHEMA_FILE = BASE_DIR.joinpath('sql_schema_db/movies_database.ddl')
