import asyncio
import logging
import logging.config

from sqlite_to_postgres import apply_schemadb
from sqlite_to_postgres.copier import copier
from sqlite_to_postgres.db import pg_conn_context, sqlite_conn_context
from sqlite_to_postgres.settings import settings

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


async def load_from_sqlite():
    """Основной метод загрузки данных из SQLite в Postgres."""
    sqlite_path = settings.DATABASES['sqlite']['db_path']
    pg_settings = settings.DATABASES['pg']
    logger.debug(f'BASE_DIR {settings.BASE_DIR}')
    logger.debug(f'SQLite {sqlite_path}')
    logger.debug(f'PG Settings {pg_settings}')
    async with (
        sqlite_conn_context.conn_context(sqlite_path) as read_conn,
        pg_conn_context.conn_context(pg_settings) as write_conn,
    ):
        # Применяем DDL схему к БД
        logger.debug('Applying DDL schema...')
        await apply_schemadb.apply(write_conn)

        # Таблицы в которых есть данные исключаем из списка на заполнение
        logger.debug('Fill tables...')
        tables = tuple(settings.TABLE_MAP.keys())
        for table in tables:
            row_count = await write_conn.fetchval(
                'SELECT COUNT(*) FROM content.{table}'.format(table=table),
            )

            if row_count == 0:
                continue

            logger.info(
                'Table {table} will not be copied because it has {row_count} entities'.format(
                    table=table,
                    row_count=row_count,
                ),
            )
            settings.TABLE_MAP.pop(table)

        # Переносим данные
        await copier.carry_over(
            settings.TABLE_MAP,
            read_conn,
            write_conn,
            settings.ROWS_PER_READ,
        )


if __name__ == '__main__':
    asyncio.run(load_from_sqlite())
