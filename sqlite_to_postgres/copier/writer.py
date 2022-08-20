import abc
import logging
from typing import Any

import asyncpg


class Writer(abc.ABC):
    """Абстрактный класс-писатель в таблицу БД."""

    def set_connection(self, conn: asyncpg.Connection):
        """Задать соединение с БД.

        Args:
            conn (aiosqlite.Connection): соединение
        """
        self.__conn = conn

    async def write(self, data_pack: list[Any]) -> None:
        """Писать набор строк в БД.

        Args:
            data_pack: набор строк для записи
        """
        try:
            await self.__conn.executemany(
                self._query,
                list(map(self._model_as_tuple, data_pack)),
            )
        except Exception as exception:
            logging.exception(exception)

    @property
    @abc.abstractmethod
    def _query(self) -> None:
        """Запрос к БД для записи модели."""
