from contextlib import asynccontextmanager

import aiosqlite


@asynccontextmanager
async def conn_context(db_path: str):
    """Контекстный менеджер для соединения с sqlite3.

    Args:
        db_path (str): Путь к БД

    Yields:
        Connection: соединение с БД
    """
    conn = aiosqlite.connect(db_path)
    yield conn
    conn.close()
