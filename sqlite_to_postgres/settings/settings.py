import os
from pathlib import Path

from dotenv import load_dotenv

from sqlite_to_postgres.copier import copier
from sqlite_to_postgres.settings import conf_readers, conf_writers

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


JOBS = (
    # Перенос таблицы кинопроизведений
    copier.CarryJob(
        reader=conf_readers.FilmworkReader(size=ROWS_PER_READ),
        writer=conf_writers.FilmworkWriter(),
    ),
    # Перенос таблицы персон
    copier.CarryJob(
        reader=conf_readers.PersonReader(size=ROWS_PER_READ),
        writer=conf_writers.PersonWriter(),
    ),
    # Перенос таблицы жанров
    copier.CarryJob(
        reader=conf_readers.GenreReader(size=ROWS_PER_READ),
        writer=conf_writers.GenreWriter(),
    ),
    # Перенос таблицы связи персон и кинопроизведений
    copier.CarryJob(
        reader=conf_readers.PersonFilmworkReader(size=ROWS_PER_READ),
        writer=conf_writers.PersonFilmworkWriter(),
    ),
    # Перенос таблицы связи жанров и кинопроизведений
    copier.CarryJob(
        reader=conf_readers.GenreFilmworkReader(size=ROWS_PER_READ),
        writer=conf_writers.GenreFilmworkWriter(),
    ),
)
