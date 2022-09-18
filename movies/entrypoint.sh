#!/bin/sh

#!/bin/sh

# Ожидаем запуска БД
echo "Waiting for postgres..."

until pg_isready -d $POSTGRES_DB -h $DB_HOST -p $DB_PORT -U $POSTGRES_USER
do
    sleep 3
    echo "Waiting for postgres at: $DB_HOST:$DB_PORT"
done

echo "PostgreSQL started"


if [ "$MAKE_MIGRATIONS" = "true" ] ; then
    # Создание схемы для джанго, если не создано
    python manage.py dbshell -- -c 'CREATE SCHEMA IF NOT EXISTS public;'
    
    # Применить миграции джанго
    echo "Django init migrations if nessesary..."
    python manage.py migrate --no-input
fi


# Если в системе отсутствует суперюзер, то создаём
if [ "$NEED_TO_CREATE_SUPERUSER" = "true" ] ; then
    echo "Creating superuser if there isn't any in DB..."
    cat create_superuser.py | python manage.py shell
    # Так же возможно создание из консоли командой:
    # DJANGO_SUPERUSER_PASSWORD=123123 \
    # DJANGO_SUPERUSER_EMAIL=mail@mail.ru \
    # python manage.py createsuperuser --noinput --name=SuperAdmin || true
fi


set -e

echo "Run Django..."
python manage.py runserver 0.0.0.0:8000 --insecure

exec "$@"