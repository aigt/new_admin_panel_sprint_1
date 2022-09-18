"""Адаптеры для преобразования моделей и значений полей к формату конечной БД.

Например для преобразования формата дат, добавления/удаления полей или
присваивания значений по умолчанию для полей которые не должны быть нулевыми.
"""

import datetime
from dataclasses import field


def adapt_timestamps(old_fields, field_values):
    """Адаптация полей с данными о времени создания и изменений.

    1. Переименование полей
         created_at  в  created
         updated_at  в  modified
    2. Приведение к стандартному формату с которым работает новая база

    Args:
        old_fields: исходные поля датаклассов
        field_values: значения полей

    Returns:
        tuple: обновлённые поля, значения
    """
    model_fields = {}
    new_values = {}
    for key, field_value in old_fields.items():
        if key == 'created_at':
            model_fields['created'] = (
                'created',
                datetime.datetime,
                field(default_factory=datetime.datetime.utcnow),
            )
            new_values['created'] = datetime.datetime.strptime(
                field_values[key] + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
            continue

        if key == 'updated_at':
            model_fields['modified'] = (
                'modified',
                datetime.datetime,
                field(default_factory=datetime.datetime.utcnow),
            )
            new_values['modified'] = datetime.datetime.strptime(
                field_values[key] + '00',
                '%Y-%m-%d %H:%M:%S.%f%z',
            )
            continue

        model_fields[key] = field_value
        new_values[key] = field_values[key]
    return model_fields, new_values


def adapt_film_work_file_path(old_fields, field_values):
    """Согласно ТЗ у данное поле отсутствует в таблице.

    Поле file_path исключается

    Args:
        old_fields: исходные поля датаклассов
        field_values: значения полей

    Returns:
        tuple: обновлённые поля, значения
    """
    model_fields = {}
    new_values = {}
    for key, field_value in old_fields.items():
        if key == 'file_path':
            continue
        model_fields[key] = field_value
        new_values[key] = field_values[key]
    return model_fields, new_values


def adapt_genre_description(old_fields, field_values):
    """Согласно ТЗ у жанров поле description не может быть null.

    Поле description с нулевыми значениями приводится к пустой строке

    Args:
        old_fields: исходные поля датаклассов
        field_values: значения полей

    Returns:
        tuple: обновлённые поля, значения
    """
    model_fields = {}
    new_values = {}
    for key, field_value in old_fields.items():
        if key == 'description' and field_values[key] is None:
            model_fields[key] = field_value
            new_values[key] = ''
            continue
        model_fields[key] = field_value
        new_values[key] = field_values[key]
    return model_fields, new_values
