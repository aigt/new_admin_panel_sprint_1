"""Модели приложения."""

import datetime
import uuid
from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Genre:
    """Жанр."""

    name: str
    description: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True, slots=True)
class Person:
    """Персона."""

    full_name: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True, slots=True)
class FilmWork:
    """Кинопроизведения."""

    title: str
    description: str
    creation_date: datetime.date | None
    type: str
    file_path: str
    created_at: datetime.datetime
    updated_at: datetime.datetime
    rating: float = field(default=0.0)  # noqa: WPS358
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True, slots=True)
class GenreFilmWork:
    """Промежуточная таблица для связи жанров и кинопроизведений."""

    film_work_id: uuid.UUID
    genre_id: uuid.UUID
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)


@dataclass(frozen=True, slots=True)
class PersonFilmWork:
    """Промежуточная таблица для связи персон и кинопроизведений."""

    person_id: uuid.UUID
    film_work_id: uuid.UUID
    role: str
    created_at: datetime.datetime
    id: uuid.UUID = field(default_factory=uuid.uuid4)
