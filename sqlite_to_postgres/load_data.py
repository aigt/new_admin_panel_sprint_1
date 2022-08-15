import sqlite3

import psycopg2
import settings
from psycopg2.extensions import connection as _connection
from psycopg2.extras import DictCursor


def load_from_sqlite(connection: sqlite3.Connection, pg_conn: _connection):
    """Основной метод загрузки данных из SQLite в Postgres.

    Args:
        connection: sqlite3 Connection
        pg_conn: Postgres Connection
    """
    # postgres_saver = PostgresSaver(pg_conn)
    # sqlite_loader = SQLiteLoader(connection)

    # data = sqlite_loader.load_movies()
    # postgres_saver.save_all_data(data)


if __name__ == '__main__':
    dsl = settings.DATABASES['pg']
    sqlite_db_path = settings.DATABASES['sqlite']['db_path']

    with (
        sqlite3.connect(sqlite_db_path) as sqlite_conn,
        psycopg2.connect(**dsl, cursor_factory=DictCursor) as pg_conn,
    ):
        load_from_sqlite(sqlite_conn, pg_conn)
