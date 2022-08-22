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
    ) -> models.FilmWork:
        attrs = self._build_attrs(cursor, row)
        return models.FilmWork(**attrs)

    @property
    def _fetch_query(self) -> str:
        return 'SELECT * FROM film_work;'


class PersonReader(reader.Reader):
    """Читатель таблицы персон."""

    def _row_factory(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> models.Person:
        attrs = self._build_attrs(cursor, row)
        return models.Person(**attrs)

    @property
    def _fetch_query(self) -> str:
        return 'SELECT * FROM "person";'


class GenreReader(reader.Reader):
    """Читатель таблицы жанров."""

    def _row_factory(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> models.Person:
        attrs = self._build_attrs(cursor, row)
        return models.Genre(**attrs)

    @property
    def _fetch_query(self) -> str:
        return 'SELECT * FROM genre;'


class PersonFilmworkReader(reader.Reader):
    """Читатель таблицы связи персон и кинопроизведений."""

    def _row_factory(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> models.Person:
        attrs = self._build_attrs(cursor, row)
        return models.PersonFilmWork(**attrs)

    @property
    def _fetch_query(self) -> str:
        return 'SELECT * FROM person_film_work;'


class GenreFilmworkReader(reader.Reader):
    """Читатель таблицы связи жанров и кинопроизведений."""

    def _row_factory(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> models.Person:
        attrs = self._build_attrs(cursor, row)
        return models.GenreFilmWork(**attrs)

    @property
    def _fetch_query(self) -> str:
        return 'SELECT * FROM genre_film_work;'
