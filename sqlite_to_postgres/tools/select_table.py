import asyncio

import aiosqlite

from sqlite_to_postgres import reader, sqlite_conn_context

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


if __name__ == '__main__':
    asyncio.run(show2())
