from contextlib import asynccontextmanager

import asyncpg


@asynccontextmanager
async def conn_context(db_settings: dict):
    """Контекстный менеджер для соединения с postgres.

    Args:
        db_settings (str): Настройки БД

    Yields:
        Connection: соединение с БД
    """
    conn = await asyncpg.connect(**db_settings)
    yield conn
    await conn.close()
