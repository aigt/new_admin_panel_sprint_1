import abc
from operator import itemgetter
from typing import Any

import aiosqlite

from sqlite_to_postgres import models, sqlite_conn_context


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
        self._size = size

    async def read(self) -> list[Any]:
        """Читать набор строк из БД (количество определено в свойстве size).

        Yields:
            list[Any]: считанный набор строк
        """
        async with sqlite_conn_context.conn_context(self._db_path) as conn:
            conn.row_factory = self._row_factory
            async with conn.execute(self._fetch_query) as curs:
                curs.arraysize = int(self._size)
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

    @property
    def _size(self) -> int:
        """Количество строк для чтения за раз.

        Returns:
            int: Количество строк для чтения за раз
        """
        return self.__size

    @_size.setter
    def _size(self, size_value: int):
        """Сеттер количества строк для чтения за раз.

        Args:
            size_value (int): Количество строк для чтения за раз.
        """
        self.__size = size_value  # noqa: WPS112

    @property
    def _db_path(self) -> str:
        """Путь к БД.

        Returns:
            str: Путь к БД
        """
        return self.__db_path


class FilmworkReader(Reader):
    """Читатель таблицы кинопроизведений."""

    def __init__(self, db_path: str, *, size: int = 1) -> None:
        """Конструктор.

        Args:
            db_path (str): Путь к БД.
            size (int): Количество считываемых рядов за раз. По умолчанию = 1.
        """
        super().__init__(db_path=db_path, size=size)

    def _row_factory(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> models.Filmwork:
        """Фабрика преобразующая строки таблиц в датакласс Filmwork.

        Args:
            cursor (aiosqlite.Cursor): курсор базы данных
            row (tuple[Any]): строка таблицы БД

        Returns:
            models.Filmwork: датакласс Filmwork
        """
        attrs = self._build_attrs(cursor, row)
        return models.Filmwork(**attrs)

    @property
    def _fetch_query(self) -> str:
        """Запрос к БД.

        Returns:
            str: Запрос к БД
        """
        return 'SELECT * FROM film_work;'
