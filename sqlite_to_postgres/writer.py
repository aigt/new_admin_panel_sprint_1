import abc
from typing import Any

import asyncpg

from sqlite_to_postgres import models, pg_conn_context


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
        async with pg_conn_context.conn_context(self._db_settings) as conn:
            await self._execute_query(
                conn,
                data_pack,
            )

    @abc.abstractmethod
    async def _execute_query(
        self,
        conn: asyncpg.Connection,
        data_pack: list[Any],
    ) -> None:
        """Запустить запись.

        Args:
            conn (asyncpg.Connection): Соединение с БД
            data_pack (list[Any]):  набор строк для записи
        """

    @property
    def _db_settings(self) -> dict:
        return self.__db_settings


class FilmworkWriter(Writer):
    """Класс-писатель для записи кинопроизведений в таблицу БД."""

    async def _execute_query(
        self,
        conn: asyncpg.Connection,
        data_pack: list[models.Filmwork],
    ) -> None:
        """Запустить запись.

        Args:
            conn (asyncpg.Connection): Соединение с БД
            data_pack (list[Any]):  набор строк для записи
        """
        await conn.executemany(
            """INSERT INTO film_work(
                id,
                title,
                description,
                creation_date,
                rating,
                type,
                created,
                modified
            )
            VALUES($1, $2, $3, $4, $5, $6, $7, $8);""",
            list(map(self._model_as_tuple, data_pack)),
        )

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
