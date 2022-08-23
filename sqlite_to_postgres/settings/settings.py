import os
from pathlib import Path

from dotenv import load_dotenv

from sqlite_to_postgres.db import models
from sqlite_to_postgres.settings import writer_adapters

# Директория приложения
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Загрузка настроек в окружение
load_dotenv(dotenv_path=BASE_DIR.joinpath('config/.env'))


# Количество записей обрабатываемых за раз
ROWS_PER_READ = 100


DATABASES = {
    'pg': {
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', '127.0.0.1'),
        'port': os.environ.get('DB_PORT', 5432),  # noqa: WPS432
    },
    'sqlite': {
        'db_path': 'sqlite_to_postgres/db.sqlite',
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
