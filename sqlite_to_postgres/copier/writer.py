import abc
from typing import Any

from sqlite_to_postgres.db import pg_conn_context


class Writer(abc.ABC):
    """Абстрактный класс-писатель в таблицу БД."""

    def __init__(self, db_settings: dict) -> None:
        """Конструктор.

        Args:
            db_settings (dict): Настройки БД
        """
        super().__init__()
        self.__db_settings = db_settings

    async def write(self, data_pack: list[Any]) -> None:
        """Писать набор строк в БД.

        Args:
            data_pack: набор строк для записи
        """
        async with pg_conn_context.conn_context(self.__db_settings) as conn:
            await conn.executemany(
                self._query,
                list(map(self._model_as_tuple, data_pack)),
            )

    @property
    @abc.abstractmethod
    def _query(self) -> None:
        """Запрос к БД для записи модели."""
