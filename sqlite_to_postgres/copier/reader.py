import abc
from operator import itemgetter
from typing import Any

import aiosqlite


class Reader(abc.ABC):
    """Абстрактный класс-читатель таблицы из БД."""

    def __init__(self, *, size=1) -> None:
        """Конструктор.

        Args:
            size (int, optional): Количество считываемых рядов за раз. По
                                  умолчанию = 1.
        """
        self.__size = size

    async def read(self) -> list[Any]:
        """Читать набор строк из БД (количество определено в свойстве size).

        Yields:
            list[Any]: считанный набор строк
        """
        self.__conn.row_factory = self._row_factory
        async with self.__conn.execute(self._fetch_query) as curs:
            curs.arraysize = int(self.__size)
            selected_data = await curs.fetchmany()
            while selected_data:
                yield selected_data
                selected_data = await curs.fetchmany()

    def set_connection(self, conn: aiosqlite.Connection):
        """Задать соединение с БД.

        Args:
            conn (aiosqlite.Connection): соединение
        """
        self.__conn = conn

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
