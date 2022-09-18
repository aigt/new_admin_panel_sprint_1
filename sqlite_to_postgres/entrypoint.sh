#!/bin/sh

# Ожидаем запуска БД
echo "Waiting for postgres..."

until pg_isready -d $POSTGRES_DB -h $DB_HOST -p $DB_PORT -U $POSTGRES_USER
do
    sleep 5
    echo "Waiting for postgres at: $DB_HOST:$DB_PORT"
done

echo "PostgreSQL started"


# Очистка БД
if [ "$CLEAN_DB" = "true" ] ; then
    echo 'Cleaning database'
    python -m clear_db
fi


# Если БД пустая, то применить схему и загрузить данные
if [ "$COPY_DATA_IN_DB" = "true" ] ; then
    echo "Controling DB consistensy and applying changes if nessesary..."
    python -m load_data
fi


# Если БД пустая, то применить схему и загрузить данные
if [ "$TEST_DB_CONSISTENSY" = "true" ] ; then
    echo "Test DB consistensy..."
    python -m pytest -s -vv ./tests/check_consistency
fi


exec "$@"