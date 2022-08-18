import abc
from operator import itemgetter
from typing import Any

import aiosqlite

from sqlite_to_postgres import models, sqlite_conn_context


class Reader(abc.ABC):
    """Абстрактный класс-читатель таблицы из БД."""

    def __init__(self, *, size=1) -> None:
        """Конструктор.

        Args:
            size (int, optional): Количество считываемых рядов за раз.
                Defaults to 1.
        """
        self.size = size

    @abc.abstractmethod
    def row_factory(self, cursor: aiosqlite.Cursor, row: tuple[Any]) -> Any:
        """Фабрика преобразующая строки таблиц в датакласс.

        Args:
            cursor (aiosqlite.Cursor): курсор базы данных
            row (tuple[Any]): строка таблицы БД

        Returns:
            Any: датакласс
        """

    async def read(self) -> list[Any]:
        """Читать набор строк из БД (количество определено в свойстве size).

        Yields:
            list[Any]: считанный набор строк
        """
        async with sqlite_conn_context.conn_context(self.db_path) as conn:
            conn.row_factory = self.row_factory
            async with conn.execute(self.fetch_query) as curs:
                curs.arraysize = int(self.size)
                selected_data = await curs.fetchmany()
                while selected_data:
                    yield selected_data
                    selected_data = await curs.fetchmany(self.size)

    @property
    def size(self) -> int:
        """Количество строк для чтения за раз.

        Returns:
            int: Количество строк для чтения за раз
        """
        return self.__size

    @size.setter
    def size(self, size_value: int):
        """Сеттер количества строк для чтения за раз.

        Args:
            size_value (int): Количество строк для чтения за раз.
        """
        self.__size = size_value  # noqa: WPS112

    @property
    @abc.abstractmethod
    def db_path(self) -> str:
        """Путь к базе данных."""

    @property
    @abc.abstractmethod
    def fetch_query(self) -> str:
        """Запрос к БД."""


class FilmworkReader(Reader):
    """Читатель таблицы кинопроизведений."""

    def __init__(self, db_path: str, *, size: int = 1) -> None:
        """Конструктор.

        Args:
            db_path (str): Путь к БД.
            size (int): Количество считываемых рядов за раз. Defaults to 1.
        """
        super().__init__(size=size)
        self.__db_path = db_path  # noqa: WPS112

    def row_factory(
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
        col_names = tuple(
            map(itemgetter(0), cursor.description),
        )

        attrs = {key: col_val for key, col_val in zip(col_names, row)}

        return models.Filmwork(**attrs)

    @property
    def db_path(self) -> str:
        """Путь к БД.

        Returns:
            str: Путь к БД
        """
        return self.__db_path

    @property
    def fetch_query(self) -> str:
        """Запрос к БД.

        Returns:
            str: Запрос к БД
        """
        return 'SELECT * FROM film_work;'
