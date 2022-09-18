import os
import sqlite3
from pathlib import Path

import psycopg2
import pytest
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor

# Директория приложения
BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent


# Загрузка настроек в окружение
load_dotenv(dotenv_path=BASE_DIR.joinpath('config/.env'))

DATABASES = {
    'pg': {
        'database': os.environ.get('DB_NAME'),
        'user': os.environ.get('DB_USER'),
        'password': os.environ.get('DB_PASSWORD'),
        'host': os.environ.get('DB_HOST', 'postgres'),
        'port': os.environ.get('DB_PORT', 5432),  # noqa: WPS432
    },
    'sqlite': {
        'db_path': BASE_DIR.joinpath('sqlite_to_postgres/db.sqlite'),
    },
}


@pytest.fixture
def lite_conn_context():
    db_path = DATABASES['sqlite']['db_path']
    conn = sqlite3.connect(db_path)
    try:
        conn.row_factory = sqlite3.Row
        yield conn
    finally:
        conn.close()


@pytest.fixture
def lite_transaction(lite_conn_context: sqlite3.Connection):
    curs = lite_conn_context.cursor()
    try:
        yield curs
        lite_conn_context.commit()
    except:
        lite_conn_context.rollback()


@pytest.fixture
def pg_conn_context():
    dbs = DATABASES['pg']
    conn = psycopg2.connect(**dbs, cursor_factory=RealDictCursor)
    try:
        yield conn
    finally:
        conn.close()


@pytest.fixture
def pg_transaction(pg_conn_context):
    curs = pg_conn_context.cursor()
    try:
        yield curs
        pg_conn_context.commit()
    except:
        pg_conn_context.rollback()
