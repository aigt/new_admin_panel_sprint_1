FROM python:3.10

ARG APP_USER=appuser
ARG APP_USER_UID=1000
ARG APP_ROOT=/app
RUN useradd --create-home --uid=${APP_USER_UID} ${APP_USER}

RUN apt-get update \
    && apt-get install build-essential python-dev -y \
    && apt-get install postgresql-client -y \
    && pip install --upgrade pip \
    && pip install "poetry==1.2.0" \
    && poetry config virtualenvs.create false

WORKDIR ${APP_ROOT}

EXPOSE 8000/tcp

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DJANGO_SETTINGS_MODULE="movies_admin.settings" \
    DJANGO_ENV=production

# Установка зависимостей
COPY pyproject.toml entrypoint.sh ./
RUN poetry install --only main --no-interaction --no-ansi

COPY --chown=${APP_USER}:${APP_USER} ./app ${APP_ROOT}

# Настройка папки статических файлов
RUN mkdir -p ${APP_ROOT}/static/ \
    && chmod -R 755 ${APP_ROOT}/static/ \
    # Настройка папки медиа файлов
    && mkdir -p ${APP_ROOT}/media/ \
    && chmod -R 755 ${APP_ROOT}/media/ \
    # Собрать статику и удалить конфиг с временными переменными окружения
    && python3 manage.py collectstatic --no-input --clear \
    && chown ${APP_USER}: ${APP_ROOT}/static/ \
    && chown ${APP_USER}: ${APP_ROOT}/media/ \
    # Точка входа
    && chmod +x ${APP_ROOT}/entrypoint.sh

USER ${APP_USER}:${APP_USER}

ENTRYPOINT [ "${APP_ROOT}/entrypoint.sh" ]