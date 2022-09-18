"""Модуль очистки БД."""

import logging
import logging.config
from contextlib import contextmanager

import psycopg2
from dotenv import load_dotenv
from psycopg2.extras import RealDictCursor
from sqlite_to_postgres.settings import settings

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


@contextmanager
def pg_conn_context():
    dbs = settings.DATABASES['pg']
    logger.debug('Connecting to DB...')
    conn = psycopg2.connect(**dbs, cursor_factory=RealDictCursor)
    try:
        logger.debug('Connectiion successful')
        yield conn
    finally:
        logger.debug('Closing connection to DB...')
        conn.close()
        logger.debug('DB connection closed')


@contextmanager
def pg_transaction(pg_conn_context):
    curs = pg_conn_context.cursor()
    try:
        logger.debug('DB cursor recieved')

        yield curs

        logger.debug('Commiting to DB...')
        pg_conn_context.commit()
        logger.debug('DB commit succesful')

    except:
        logger.exception('DB commit is being rolled back because of exception ...')
        pg_conn_context.rollback()
        logger.exception('DB commit is rolled back')


def clear():
    with pg_conn_context() as conn:
        with pg_transaction(conn) as curs:
            logger.debug('Dropping content schema...')
            curs.execute('DROP SCHEMA IF EXISTS content CASCADE;')
            logger.info('Content schema is dropped')

            logger.debug('Dropping public schema...')
            curs.execute('DROP SCHEMA IF EXISTS public CASCADE;')
            logger.info('Public schema is dropped')


if __name__ == '__main__':
    logger.debug('Clearing of DB is being started...')
    clear()
    logger.debug('Clearing of DB finished')
