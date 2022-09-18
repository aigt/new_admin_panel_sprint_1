import pytest
from psycopg2.extensions import AsIs


def test_compare_counts(lite_transaction, pg_transaction):

    tables_list = (
        'film_work',
        'person',
        'genre',
        'person_film_work',
        'genre_film_work',
    )

    for table in tables_list:
        pg_transaction.execute('SELECT COUNT(*) FROM %s', (AsIs(table),))
        pg_count = pg_transaction.fetchone()['count']
        lite_transaction.execute('SELECT COUNT(*) FROM %s' % table)
        lite_count = lite_transaction.fetchone()[0]
        assert pg_count == lite_count
