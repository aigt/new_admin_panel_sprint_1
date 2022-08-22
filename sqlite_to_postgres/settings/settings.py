import os
from pathlib import Path

from dotenv import load_dotenv

from sqlite_to_postgres.copier import copier, reader
from sqlite_to_postgres.db import models
from sqlite_to_postgres.settings import conf_writers

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
    'film_work': models.FilmWork,
    'person': models.Person,
    'genre': models.Genre,
    'person_film_work': models.PersonFilmWork,
    'genre_film_work': models.GenreFilmWork,
}


JOBS = (
    # Перенос таблицы кинопроизведений
    copier.CarryJob(
        reader=reader.Reader(
            'film_work',
            schema=models.FilmWork,
            size=ROWS_PER_READ,
        ),
        writer=conf_writers.FilmworkWriter(),
    ),
    # Перенос таблицы персон
    copier.CarryJob(
        reader=reader.Reader(
            'person',
            schema=models.Person,
            size=ROWS_PER_READ,
        ),
        writer=conf_writers.PersonWriter(),
    ),
    # Перенос таблицы жанров
    copier.CarryJob(
        reader=reader.Reader(
            'genre',
            schema=models.Genre,
            size=ROWS_PER_READ,
        ),
        writer=conf_writers.GenreWriter(),
    ),
    # Перенос таблицы связи персон и кинопроизведений
    copier.CarryJob(
        reader=reader.Reader(
            'person_film_work',
            schema=models.PersonFilmWork,
            size=ROWS_PER_READ,
        ),
        writer=conf_writers.PersonFilmworkWriter(),
    ),
    # Перенос таблицы связи жанров и кинопроизведений
    copier.CarryJob(
        reader=reader.Reader(
            'genre_film_work',
            schema=models.GenreFilmWork,
            size=ROWS_PER_READ,
        ),
        writer=conf_writers.GenreFilmworkWriter(),
    ),
)
