import abc
from operator import itemgetter
from typing import Any

import aiosqlite

from sqlite_to_postgres.db import sqlite_conn_context


class Reader(abc.ABC):
    """Абстрактный класс-читатель таблицы из БД."""

    def __init__(self, db_path: str, *, size=1) -> None:
        """Конструктор.

        Args:
            db_path (str): Путь к БД.
            size (int, optional): Количество считываемых рядов за раз. По
                                  умолчанию = 1.
        """
        self.__db_path = db_path  # noqa: WPS112
        self.__size = size

    async def read(self) -> list[Any]:
        """Читать набор строк из БД (количество определено в свойстве size).

        Yields:
            list[Any]: считанный набор строк
        """
        async with sqlite_conn_context.conn_context(self.__db_path) as conn:
            conn.row_factory = self._row_factory
            async with conn.execute(self._fetch_query) as curs:
                curs.arraysize = int(self.__size)
                selected_data = await curs.fetchmany()
                while selected_data:
                    yield selected_data
                    selected_data = await curs.fetchmany()

    def _build_attrs(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> dict:
        """Фабрика преобразующая строки таблиц в словарь.

        Args:
            cursor (aiosqlite.Cursor): курсор базы данных
            row (tuple[Any]): строка таблицы БД

        Returns:
            dict: словарь с атрибутами для создания класса
        """
        col_names = tuple(
            map(itemgetter(0), cursor.description),
        )

        return {key: col_val for key, col_val in zip(col_names, row)}

    @abc.abstractmethod
    def _row_factory(self, cursor: aiosqlite.Cursor, row: tuple[Any]) -> Any:
        """Фабрика преобразующая строки таблиц в датакласс.

        Args:
            cursor (aiosqlite.Cursor): курсор базы данных
            row (tuple[Any]): строка таблицы БД

        Returns:
            Any: датакласс
        """

    @property
    @abc.abstractmethod
    def _fetch_query(self) -> str:
        """Запрос к БД."""
