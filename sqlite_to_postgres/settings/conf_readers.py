"""Конфигурации ридеров."""

from typing import Any

import aiosqlite

from sqlite_to_postgres.copier import reader
from sqlite_to_postgres.db import models


class FilmworkReader(reader.Reader):
    """Читатель таблицы кинопроизведений."""

    def _row_factory(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> models.Filmwork:
        attrs = self._build_attrs(cursor, row)
        return models.Filmwork(**attrs)

    @property
    def _fetch_query(self) -> str:
        return 'SELECT * FROM film_work;'
