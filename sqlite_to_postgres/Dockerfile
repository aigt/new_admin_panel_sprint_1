FROM python:3.10

RUN apt-get update \
    && apt-get install build-essential python-dev -y \
    && apt-get install postgresql-client -y \
    && pip install --upgrade pip \
    && pip install "poetry==1.2.0" \
    && poetry config virtualenvs.create false

WORKDIR /opt/app

# Переменные окружения
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PROD_ENV=production \
    CLEAN_DB=false \
    COPY_DATA_IN_DB=true \
    TEST_DB_CONSISTENSY=true

# Установка зависимостей
COPY pyproject.toml entrypoint.sh ./
RUN poetry install --only main --no-interaction --no-ansi

COPY ./app .

RUN groupadd -r web \
    && useradd -d /opt/app -r -g web web \
    && chmod +x entrypoint.sh \
    && chown web:web -R /opt/app

USER web

ENTRYPOINT [ "/opt/app/entrypoint.sh" ]