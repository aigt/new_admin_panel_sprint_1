"""Модуль копирует данные из одной базы данных в другую.

Каждая копируемая таблица заносится в свою работу.
После чего все работы запускаются методом carry_over().
"""

import asyncio

import aiosqlite
import asyncpg

from copier import reader, writer


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
    """Читай данные из очереди и пиши их в БД.

    Args:
        queue (asyncio.Queue): очередь
        db_writer (writer.Writer): писатель в БД
    """
    while True:
        data_pack = await queue.get()
        await db_writer.write(data_pack)
        queue.task_done()


async def _produce_job(
    db_reader: reader.Reader,
    db_writer: writer.Writer,
) -> None:
    """Выполнить работу.

    Args:
        db_reader (reader.Reader): Читатель из БД
        db_writer (reader.Writer): Писатель в БД
    """
    # Создать очередь через которую будут передаваться данные.
    queue = asyncio.Queue(maxsize=10)

    # Создать таск для чтения бд.
    reader_task = asyncio.create_task(_read(queue, db_reader))

    # Создать таск для записи в бд.
    writer_task = asyncio.create_task(_write(queue, db_writer))

    # Ожидаем пока все данные будут прочитаны
    await asyncio.wait({reader_task})

    # Затем ждём пока все данные из очереди будут записаны
    await queue.join()

    # Отменить таск записи в бд и дождаться отмены.
    writer_task.cancel()
    await asyncio.wait({writer_task})


async def carry_over(
    table_maps: dict,
    read_conn: aiosqlite.Connection,
    write_conn: asyncpg.Connection,
    rows_per_read: int,
) -> None:
    """Выполнить список работ по копированию данных.

    Args:
        table_maps (dict): список работ
        read_conn (aiosqlite.Connection): Соединение с БД источником данных
        write_conn (asyncpg.Connection): Соединение с БД для записи данных
        rows_per_read (int): Количество считываемых рядов за раз
    """
    # Копирование каждой таблицы выполняется как отдельная работа
    for table_name, tmap in table_maps.items():
        db_reader = reader.Reader(
            table_name,
            schema=tmap[0],
            size=rows_per_read,
            connection=read_conn,
        )
        db_writer = writer.Writer(
            table_name,
            adapters=tmap[1],
            connection=write_conn,
        )
        await _produce_job(db_reader, db_writer)
