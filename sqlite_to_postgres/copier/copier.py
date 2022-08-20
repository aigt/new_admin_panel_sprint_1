"""Модуль копирует данные из одной базы данных в другую.

Каждая копируемая таблица заносится в свою работу CarryJob.
После чего все работы запускаются методом carry_over().
"""

import asyncio
from dataclasses import dataclass
from typing import Iterable

from sqlite_to_postgres.copier import reader, writer


@dataclass(frozen=True, slots=True)
class CarryJob:
    """Данные для выполнения работы по копированию таблицы БД."""

    reader: reader.Reader
    writer: writer.Writer


async def _read(
    queue: asyncio.Queue,
    db_reader: reader.Reader,
) -> None:
    """Читать данные из db_reader и передавать их в очередь.

    Args:
        queue (asyncio.Queue): очередь
        db_reader (reader.Reader): читатель из БД
    """
    async for data_pack in db_reader.read():
        await queue.put(data_pack)


async def _write(
    queue: asyncio.Queue,
    db_writer: writer.Writer,
) -> None:
    """Читай данные из очереди и пиши из в БД.

    Args:
        queue (asyncio.Queue): очередь
        db_writer (writer.Writer): писатель в БД
    """
    while True:
        data_pack = await queue.get()
        await db_writer.write(data_pack)
        queue.task_done()


async def _produce_job(job: CarryJob) -> None:
    """Выполнить работу.

    Args:
        job (CarryJob): Информация для выполнения работы по копированию данных
    """
    # Создать очередь через которую будут передаваться данные.
    queue = asyncio.Queue(maxsize=10)

    # Создать таск для чтения бд.
    db_reader = asyncio.create_task(_read(queue, job.reader))

    # Создать таск для записи в бд.
    db_writer = asyncio.create_task(_write(queue, job.writer))

    # Ожидаем пока все данные будут прочитаны
    await asyncio.wait({db_reader})

    # Затем ждём пока все данные из очереди будут записаны
    await queue.join()

    # Отменить таск записи в бд и дождаться отмены.
    db_writer.cancel()
    await asyncio.wait({db_writer})


async def carry_over(jobs: Iterable[CarryJob]) -> None:
    """Выполнить список работ по копированию данных.

    Args:
        jobs (Iterable[CarryJob]): список работ
    """
    # Копирование каждой таблицы выполняется как отдельная работа
    for job in jobs:
        await _produce_job(job)
