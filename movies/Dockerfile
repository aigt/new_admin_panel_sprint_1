FROM python:3.10

RUN apt-get update \
    && apt-get install build-essential python-dev -y \
    && apt-get install postgresql-client -y \
    && pip install --upgrade pip \
    && pip install "poetry==1.2.0" \
    && poetry config virtualenvs.create false

WORKDIR /opt/app

# Укажите порт, на котором приложение будет доступно внутри Docker-сети
EXPOSE 8000/tcp

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE="movies_admin.settings" \
    DJANGO_ENV=production

# Установка зависимостей
COPY pyproject.toml entrypoint.sh ./
RUN poetry install --only main --no-interaction --no-ansi

COPY ./app .

RUN groupadd -r web \
    && useradd -d /opt/app -r -g web web \
    # Настройка папки статических файлов
    && mkdir -p /opt/app/static/ \
    && chmod -R 755 /opt/app/static/ \
    && chown web: /opt/app/static/ \
    # Настройка папки медиа файлов
    && mkdir -p /opt/app/media/ \
    && chmod -R 755 /opt/app/media/ \
    && chown web: /opt/app/media/ \
    # Собрать статику и удалить конфиг с временными переменными окружения
    && python3 manage.py collectstatic --no-input --clear \
    # Точка входа
    && chmod +x entrypoint.sh \
    && chown web:web -R /opt/app

USER web

ENTRYPOINT [ "/opt/app/entrypoint.sh" ]