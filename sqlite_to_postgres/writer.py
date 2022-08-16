import abc
from typing import Any


class Writer(abc.ABC):
    """Абстрактный класс-писатель в таблицу БД."""

    @abc.abstractmethod
    async def write(self, data_pack: list[Any]) -> None:
        """Писать набор строк в БД.

        Args:
            data_pack: набор строк для записи
        """
