import asyncio
import datetime
import uuid

import aiosqlite

from sqlite_to_postgres.copier import copier
from sqlite_to_postgres.db import models, sqlite_conn_context
from sqlite_to_postgres.settings import conf_readers, conf_writers, settings

ROWS_PER_READ = 5


async def show():
    """Отобразить таблицу БД."""
    db_path = 'sqlite_to_postgres/db.sqlite'

    async with sqlite_conn_context.conn_context(db_path) as conn:
        print(conn)
        conn.row_factory = aiosqlite.Row
        async with conn.execute('SELECT * FROM film_work;') as curs:
            # Получаем данные
            selected_data = await curs.fetchall()
            # Рассматриваем первую запись
            print(dict(selected_data[0]))


async def show2():
    """Отобразить таблицу БД с помощью ридера и моделей."""
    db_path = 'sqlite_to_postgres/db.sqlite'
    fwr = conf_readers.FilmworkReader(db_path, size=ROWS_PER_READ)
    async for fw_models in fwr.read():
        print(*fw_models, sep='\n\n', end='\n\n**************\n\n')


async def insert_values():
    """Записать в таблицу тестовые данные."""
    dbs = settings.DATABASES['pg']
    model = models.Filmwork(
        id=str(uuid.uuid4()),
        title='Название1',
        description='Описание2',
        creation_date=datetime.datetime.today(),
        rating=5.6,  # noqa: WPS432
        type='tv_show',
        file_path='',
        created_at=datetime.datetime.utcnow(),
        updated_at=datetime.datetime.utcnow(),
    )
    db_writer = conf_writers.FilmworkWriter(dbs)
    async with db_writer.create_writing_context():
        await db_writer.write([model])


async def copy():
    """Копирование из одной базы в другую."""
    db_path = 'sqlite_to_postgres/db.sqlite'
    db_reader = conf_readers.GenreFilmworkReader(db_path, size=ROWS_PER_READ)

    dbs = settings.DATABASES['pg']
    db_writer = conf_writers.GenreFilmworkWriter(dbs)

    jobs = (
        copier.CarryJob(
            reader=db_reader,
            writer=db_writer,
        ),
    )
    await copier.carry_over(jobs)


if __name__ == '__main__':
    asyncio.run(copy())
