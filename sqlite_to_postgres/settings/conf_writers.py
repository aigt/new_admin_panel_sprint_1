import datetime
import logging

from sqlite_to_postgres.copier import writer
from sqlite_to_postgres.db import models


class FilmworkWriter(writer.Writer):
    """Класс-писатель для записи кинопроизведений в таблицу БД."""

    @property
    def _query(self) -> None:
        return """INSERT INTO content.film_work(
                id,
                title,
                description,
                creation_date,
                rating,
                type,
                created,
                modified
            )
            VALUES($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT (id) DO NOTHING;"""

    def _model_as_tuple(self, model: models.FilmWork):
        try:
            created = datetime.datetime.strptime(
                model.created_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as c_ex:
            logging.exception(c_ex, 'model.created_at', model.created_at)
            created = None

        try:
            modified = datetime.datetime.strptime(
                model.updated_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as u_ex:
            logging.exception(u_ex, 'model.updated_at', model.updated_at)
            modified = None

        return (
            model.id,
            model.title,
            model.description,
            model.creation_date,
            model.rating,
            model.type,
            created,
            modified,
        )


class PersonWriter(writer.Writer):
    """Класс-писатель для записи персон в таблицу БД."""

    @property
    def _query(self) -> None:
        return """INSERT INTO content.person(
                id,
                full_name,
                created,
                modified
            )
            VALUES($1, $2, $3, $4)
            ON CONFLICT (id) DO NOTHING;"""

    def _model_as_tuple(self, model: models.Person):
        try:
            created = datetime.datetime.strptime(
                model.created_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as c_ex:
            logging.exception(c_ex, 'model.created_at', model.created_at)
            created = None

        try:
            modified = datetime.datetime.strptime(
                model.updated_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as u_ex:
            logging.exception(u_ex, 'model.updated_at', model.updated_at)
            modified = None

        return (
            model.id,
            model.full_name,
            created,
            modified,
        )


class GenreWriter(writer.Writer):
    """Класс-писатель для записи персон в таблицу БД."""

    @property
    def _query(self) -> None:
        return """INSERT INTO content.genre(
                id,
                name,
                description,
                created,
                modified
            )
            VALUES($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO NOTHING;"""

    def _model_as_tuple(self, model: models.Genre):
        try:
            created = datetime.datetime.strptime(
                model.created_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as c_ex:
            logging.exception(c_ex, 'model.created_at', model.created_at)
            created = None

        try:
            modified = datetime.datetime.strptime(
                model.updated_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as u_ex:
            logging.exception(u_ex, 'model.updated_at', model.updated_at)
            modified = None

        description = model.description
        if description is None:
            description = ''

        return (
            model.id,
            model.name,
            description,
            created,
            modified,
        )


class PersonFilmworkWriter(writer.Writer):
    """Писатель для записи связи персон и кинопроизведений в таблицу БД."""

    @property
    def _query(self) -> None:
        return """INSERT INTO content.person_film_work(
                id,
                film_work_id,
                person_id,
                role,
                created
            )
            VALUES($1, $2, $3, $4, $5)
            ON CONFLICT (id) DO NOTHING;"""

    def _model_as_tuple(self, model: models.PersonFilmWork):
        try:
            created = datetime.datetime.strptime(
                model.created_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as c_ex:
            logging.exception(c_ex, 'model.created_at', model.created_at)
            created = None

        return (
            model.id,
            model.film_work_id,
            model.person_id,
            model.role,
            created,
        )


class GenreFilmworkWriter(writer.Writer):
    """Писатель для записи связи жанров и кинопроизведений в таблицу БД."""

    @property
    def _query(self) -> None:
        return """INSERT INTO content.genre_film_work(
                id,
                film_work_id,
                genre_id,
                created
            )
            VALUES($1, $2, $3, $4)
            ON CONFLICT (id) DO NOTHING;"""

    def _model_as_tuple(self, model: models.GenreFilmWork):
        try:
            created = datetime.datetime.strptime(
                model.created_at + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
        except Exception as c_ex:
            logging.exception(c_ex, 'model.created_at', model.created_at)
            created = None

        return (
            model.id,
            model.film_work_id,
            model.genre_id,
            created,
        )
