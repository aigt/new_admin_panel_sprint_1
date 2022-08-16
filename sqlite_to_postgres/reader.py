import abc
from typing import Any


class Reader(abc.ABC):
    """Абстрактный класс-читатель таблицы из БД."""

    @abc.abstractmethod
    async def read(self) -> list[Any]:
        """Читать набор строк из БД (количество определено в свойстве size).

        Returns:
            list[Any]: считанный набор строк
        """

    @property
    @abc.abstractmethod
    def size(self) -> int:
        """Количество строк для чтения за раз."""
