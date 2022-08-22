import abc
from operator import itemgetter
from typing import Any

import aiosqlite


class Reader(abc.ABC):
    """Класс-читатель таблицы из БД."""

    def __init__(
        self,
        table_name: str,
        *,
        schema,
        size: int = 1,
    ) -> None:
        """Конструктор.

        Args:
            table_name (str): Имя читаемой таблицы
            schema: Датакласс-схема данных
            size (int, optional): Количество считываемых рядов за раз. По
                                  умолчанию = 1.
        """
        self.__size = size
        self.__table_name = table_name
        self.__schema = schema

    async def read(self) -> list[Any]:
        """Читать набор строк из БД (количество определено в свойстве size).

        Yields:
            list[Any]: считанный набор строк
        """
        self.__conn.row_factory = self._row_factory
        fetch_query = 'SELECT * FROM {table};'.format(table=self.__table_name)
        async with self.__conn.execute(fetch_query) as curs:
            curs.arraysize = self.__size
            while selected_data := await curs.fetchmany():
                yield selected_data

    def set_connection(self, conn: aiosqlite.Connection):
        """Задать соединение с БД.

        Args:
            conn (aiosqlite.Connection): соединение
        """
        self.__conn = conn

    def _row_factory(
        self,
        cursor: aiosqlite.Cursor,
        row: tuple[Any],
    ) -> Any:
        """Фабрика преобразующая строки таблиц в датакласс.

        Args:
            cursor (aiosqlite.Cursor): курсор базы данных
            row (tuple[Any]): строка таблицы БД

        Returns:
            Any: датакласс
        """
        col_names = tuple(map(itemgetter(0), cursor.description))
        attrs = {key: col_val for key, col_val in zip(col_names, row)}

        return self.__schema(**attrs)
