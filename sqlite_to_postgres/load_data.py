import asyncio

from sqlite_to_postgres.copier import copier
from sqlite_to_postgres.db import pg_conn_context, sqlite_conn_context
from sqlite_to_postgres.settings import settings


async def load_from_sqlite():
    """Основной метод загрузки данных из SQLite в Postgres."""
    sqlite_path = settings.DATABASES['sqlite']['db_path']
    pg_settings = settings.DATABASES['pg']
    async with (
        sqlite_conn_context.conn_context(sqlite_path) as rconn,
        pg_conn_context.conn_context(pg_settings) as wconn,
    ):
        for job in settings.JOBS:
            job.reader.set_connection(rconn)
            job.writer.set_connection(wconn)
        await copier.carry_over(settings.JOBS)


if __name__ == '__main__':
    asyncio.run(load_from_sqlite())
