from sqlite_to_postgres.copier import writer
from sqlite_to_postgres.db import models


class FilmworkWriter(writer.Writer):
    """Класс-писатель для записи кинопроизведений в таблицу БД."""

    @property
    def _query(self) -> None:
        return """INSERT INTO film_work(
                id,
                title,
                description,
                creation_date,
                rating,
                type,
                created,
                modified
            )
            VALUES($1, $2, $3, $4, $5, $6, $7, $8);"""

    def _model_as_tuple(self, model: models.Filmwork):
        return (
            model.id,
            model.title,
            model.description,
            model.creation_date,
            model.rating,
            model.type,
            model.created_at,
            model.updated_at,
        )
