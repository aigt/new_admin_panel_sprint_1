import sqlite3

import psycopg2
import pytest
from psycopg2.extras import RealDictCursor
from settings import settings



DATABASES = settings.DATABASES


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
