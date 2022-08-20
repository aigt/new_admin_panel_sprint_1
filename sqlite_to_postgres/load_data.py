import asyncio

from sqlite_to_postgres.copier import copier
from sqlite_to_postgres.settings import settings


async def load_from_sqlite():
    """Основной метод загрузки данных из SQLite в Postgres."""
    await copier.carry_over(settings.JOBS)


if __name__ == '__main__':
    asyncio.run(load_from_sqlite())
