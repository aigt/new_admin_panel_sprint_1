import datetime

import pytest
from psycopg2.extensions import AsIs


def test_compare_film_work_rows(lite_transaction, pg_transaction):

    pg_query = """
        SELECT
            id,
            title,
            description,
            creation_date,
            rating,
            type,
            created,
            modified
        FROM content.film_work
        """
    lite_query = """
        SELECT
            id,
            title,
            description,
            creation_date,
            rating,
            type,
            created_at,
            updated_at
        FROM film_work
        WHERE id = ?
        """
    pg_transaction.execute(pg_query)

    for pg_row in pg_transaction:
        id = pg_row['id']
        pg_dict = dict(pg_row)
        lite_transaction.execute(lite_query, (id,))
        lite_row = lite_transaction.fetchone()
        lite_dict = dict(lite_row)
        lite_dict['created'] = datetime.datetime.strptime(
            lite_dict['created_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['created_at']
        lite_dict['modified'] = datetime.datetime.strptime(
            lite_dict['updated_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['updated_at']

        assert pg_dict == lite_dict


def test_compare_person_rows(lite_transaction, pg_transaction):

    pg_query = """
        SELECT
            id,
            full_name,
            created,
            modified
        FROM content.person
        """
    lite_query = """
        SELECT
            id,
            full_name,
            created_at,
            updated_at
        FROM person
        WHERE id = ?
        """
    pg_transaction.execute(pg_query)

    for pg_row in pg_transaction:
        id = pg_row['id']
        pg_dict = dict(pg_row)
        lite_transaction.execute(lite_query, (id,))
        lite_row = lite_transaction.fetchone()
        lite_dict = dict(lite_row)
        lite_dict['created'] = datetime.datetime.strptime(
            lite_dict['created_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['created_at']
        lite_dict['modified'] = datetime.datetime.strptime(
            lite_dict['updated_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['updated_at']

        assert pg_dict == lite_dict


def test_compare_genre_rows(lite_transaction, pg_transaction):

    pg_query = """
        SELECT
            id,
            name,
            description,
            created,
            modified
        FROM content.genre
        """
    lite_query = """
        SELECT
            id,
            name,
            description,
            created_at,
            updated_at
        FROM genre
        WHERE id = ?
        """
    pg_transaction.execute(pg_query)

    for pg_row in pg_transaction:

        id = pg_row['id']
        pg_dict = dict(pg_row)

        lite_transaction.execute(lite_query, (id,))
        lite_row = lite_transaction.fetchone()
        lite_dict = dict(lite_row)

        lite_dict['created'] = datetime.datetime.strptime(
            lite_dict['created_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['created_at']

        lite_dict['modified'] = datetime.datetime.strptime(
            lite_dict['updated_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['updated_at']

        if lite_dict['description'] is None:
            lite_dict['description'] = ''

        assert pg_dict == lite_dict


def test_compare_genre_film_work_rows(lite_transaction, pg_transaction):

    pg_query = """
        SELECT
            id,
            film_work_id,
            genre_id,
            created
        FROM content.genre_film_work
        """
    lite_query = """
        SELECT
            id,
            film_work_id,
            genre_id,
            created_at
        FROM genre_film_work
        WHERE id = ?
        """
    pg_transaction.execute(pg_query)

    for pg_row in pg_transaction:

        id = pg_row['id']
        pg_dict = dict(pg_row)

        lite_transaction.execute(lite_query, (id,))
        lite_row = lite_transaction.fetchone()
        lite_dict = dict(lite_row)

        lite_dict['created'] = datetime.datetime.strptime(
            lite_dict['created_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['created_at']

        assert pg_dict == lite_dict


def test_compare_person_film_work_rows(lite_transaction, pg_transaction):

    pg_query = """
        SELECT
            id,
            film_work_id,
            person_id,
            role,
            created
        FROM content.person_film_work
        """
    lite_query = """
        SELECT
            id,
            film_work_id,
            person_id,
            role,
            created_at
        FROM person_film_work
        WHERE id = ?
        """
    pg_transaction.execute(pg_query)

    for pg_row in pg_transaction:

        id = pg_row['id']
        pg_dict = dict(pg_row)

        lite_transaction.execute(lite_query, (id,))
        lite_row = lite_transaction.fetchone()
        lite_dict = dict(lite_row)

        lite_dict['created'] = datetime.datetime.strptime(
            lite_dict['created_at'] + '00',
            '%Y-%m-%d %H:%M:%S.%f%z',
        )
        del lite_dict['created_at']

        assert pg_dict == lite_dict
