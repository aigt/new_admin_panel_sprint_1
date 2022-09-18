import logging
import logging.config
from dataclasses import asdict, astuple, fields, make_dataclass
from typing import Any, Callable

import asyncpg
from sqlite_to_postgres.settings import settings

logging.config.dictConfig(settings.LOGGING_CONFIG)
logger = logging.getLogger(__name__)


class Writer:
    """Класс-писатель в таблицу БД."""

    def __init__(
        self,
        table_name: str,
        *,
        adapters: tuple[Callable],
        connection: asyncpg.Connection,
    ) -> None:
        """Конструктор.

        Args:
            table_name (str): Имя читаемой таблицы
            adapters (tuple[Callable]): Адаптеры моделей под конечную таблицу
            connection (asyncpg.Connection): Соединение
        """
        self.__table_name = table_name
        self.__adapters = adapters
        self.__conn = connection
        self.__query = None
        self.__schema = None

    async def write(self, data_pack: list[Any]) -> None:
        """Писать набор строк в БД.

        Args:
            data_pack: набор строк для записи
        """
        logger.debug('Preparing data pack to writing...')
        prepared_data = tuple(map(self.__adapt_fields, data_pack))
        logger.debug('Data pack is prepared to writing')

        if self.__query is None:
            logger.debug(
                'Preparing DB query for table {table}...'.format(
                    table=self.__table_name,
                ),
            )
            self.__update_query(prepared_data[0])
            logger.debug(
                'DB query is prepared:\n{query}'.format(query=self.__query),
            )

        try:
            logger.debug('Writing data pack...')
            await self.__conn.executemany(
                self.__query,
                map(astuple, prepared_data),
            )
            logger.debug(
                'Data pack is written into {table}'.format(
                    table=self.__table_name,
                ),
            )
        except asyncpg.exceptions.NullValueNotAllowedError as exception:
            logger.exception('Null Value Not Allowed Error:', exception)

    def __adapt_fields(self, model: Any):
        model_fields = {
            fi.name: (
                fi.name,
                fi.type,
                fi,
            )
            for fi in fields(model)
        }
        field_values = asdict(model)

        for adapter in self.__adapters:
            model_fields, field_values = adapter(model_fields, field_values)

        if self.__schema is None:
            self.__schema = make_dataclass(
                self.__table_name,
                model_fields,
                frozen=True,
                slots=True,
            )
            logger.debug(
                'Created new schema for table {table}: {schema}'.format(
                    table=self.__table_name,
                    schema=self.__schema,
                ),
            )

        return self.__schema(**field_values)

    def __update_query(self, schema: Any):
        """Обнови запрос к БД по схеме.

        Args:
            schema (Any): схема (датакласс), под которую будет перестроен
                          запрос
        """
        attrs = schema.__annotations__.keys()
        cols = ','.join(attrs)
        values_pattern = ','.join(
            '${num}'.format(num=num)
            for num in range(
                1,
                len(attrs) + 1,
            )
        )

        self.__query = """
            INSERT INTO content.{table}({cols})
            VALUES({values_pattern})
            ON CONFLICT (id) DO NOTHING;
        """.format(
            table=self.__table_name,
            cols=cols,
            values_pattern=values_pattern,
        )
