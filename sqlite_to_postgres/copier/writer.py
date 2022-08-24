import logging
from dataclasses import asdict, astuple, fields, make_dataclass
from typing import Any, Callable

import asyncpg


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

    async def write(self, data_pack: list[Any]) -> None:
        """Писать набор строк в БД.

        Args:
            data_pack: набор строк для записи
        """
        prepared_data = tuple(map(self.__adapt_fields, data_pack))

        if self.__query is None:
            self.__update_query(prepared_data[0])

        try:
            await self.__conn.executemany(
                self.__query,
                map(astuple, prepared_data),
            )
        except asyncpg.exceptions.NullValueNotAllowedError as exception:
            logging.exception('Попытка записи нулевого значения:', exception)

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

        new_dc = make_dataclass(self.__table_name, model_fields)
        return new_dc(**field_values)

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
