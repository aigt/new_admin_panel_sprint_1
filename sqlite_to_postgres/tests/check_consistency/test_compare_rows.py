import datetime

import pytest
from psycopg2.extensions import AsIs


def test_compare_rows(lite_transaction, pg_transaction):

    tables_list = (
        'film_work',
        'person',
        'genre',
        'person_film_work',
        'genre_film_work',
    )

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
        FROM film_work
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
        print('pg_dict', pg_dict)
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

        print('lite_dict', lite_dict)

        assert pg_dict == lite_dict
