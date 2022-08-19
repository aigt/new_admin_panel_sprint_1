import asyncio
import datetime
import uuid

import aiosqlite

from sqlite_to_postgres import (  # isort:skip
    pg_conn_context,
    reader,
    settings,
    sqlite_conn_context,
)

ROWS_PER_READ = 20


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
    fwr = reader.FilmworkReader(db_path, size=ROWS_PER_READ)
    async for fw_models in fwr.read():
        print(*fw_models, sep='\n\n', end='\n\n**************\n\n')


async def insert_values():
    """Записать в таблицу тестовые данные."""
    dbs = settings.DATABASES['pg']
    async with pg_conn_context.conn_context(dbs) as conn:
        await conn.execute(
            """INSERT INTO film_work(
                id,
                title,
                description,
                creation_date,
                rating,
                type,
                created,
                modified
            )
            VALUES($1, $2, $3, $4, $5, $6, $7, $8);""",
            str(uuid.uuid4()),
            'Название1',
            'Описание2',
            datetime.datetime.today(),
            5.6,  # noqa: WPS432
            'tv_show',
            datetime.datetime.utcnow(),
            datetime.datetime.utcnow(),
        )


if __name__ == '__main__':
    asyncio.run(insert_values())
