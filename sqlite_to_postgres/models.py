"""Модели приложения."""

import datetime
import uuid
from dataclasses import astuple, dataclass, field


@dataclass(frozen=True, slots=True)
class Genre:
    """Жанр."""

    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __iter__(self):
        return iter(astuple(self))


@dataclass(frozen=True, slots=True)
class Person:
    """Персона."""

    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __iter__(self):
        return iter(astuple(self))


@dataclass(frozen=True, slots=True)
class Filmwork:
    """Кинопроизведения."""

    title: str
    description: str
    creation_date: datetime.datetime
    type: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    rating: float = field(default=0.0)
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __iter__(self):
        return iter(astuple(self))


@dataclass(frozen=True, slots=True)
class GenreFilmwork:
    """Промежуточная таблица для связи жанров и кинопроизведений."""

    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __iter__(self):
        return iter(astuple(self))


@dataclass(frozen=True, slots=True)
class PersonFilmwork:
    """Промежуточная таблица для связи персон и кинопроизведений."""

    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)

    def __iter__(self):
        return iter(astuple(self))
