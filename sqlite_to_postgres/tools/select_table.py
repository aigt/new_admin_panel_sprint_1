import asyncio

import aiosqlite

from sqlite_to_postgres import sqlite_conn_context


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


if __name__ == '__main__':
    asyncio.run(show())
