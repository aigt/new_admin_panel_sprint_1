"""Модели прложения."""

import uuid

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

GENRE_NAME_MAX_LENGTH = 255
FILMWORK_TITLE_MAX_LENGTH = 255
PERSON_FULLNAME_MAX_LENGTH = 255


class UUIDMixin(models.Model):
    """Миксин с uuid идентификатором id."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class TimeStampedMixin(models.Model):
    """Миксин с датами создания и модификации."""

    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class Genre(UUIDMixin, TimeStampedMixin):
    """Жанр."""

    name = models.CharField(_('name'), max_length=GENRE_NAME_MAX_LENGTH)
    description = models.TextField(_('description'), blank=True)

    def __str__(self):
        """Строковое представление модели.

        Returns:
            str: Имя жанра
        """
        return self.name

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = _('genre')
        verbose_name_plural = _('genres')


class Person(UUIDMixin, TimeStampedMixin):
    """Персона."""

    full_name = models.CharField(
        _('full_name'),
        max_length=PERSON_FULLNAME_MAX_LENGTH,
    )

    def __str__(self):
        """Строковое представление модели.

        Returns:
            str: Полное имя
        """
        return self.full_name

    class Meta:
        db_table = 'content\".\"person'
        verbose_name = _('person')
        verbose_name_plural = _('persons')


class Filmwork(UUIDMixin, TimeStampedMixin):
    """Кинопроизведения."""

    class Type(models.TextChoices):
        MOVIE = ('MOVIE', _('movie'))
        TV_SHOW = ('TV_SHOW', _('tv_show'))

    title = models.CharField(_('title'), max_length=FILMWORK_TITLE_MAX_LENGTH)
    description = models.TextField(_('description'), blank=True)
    creation_date = models.DateField(_('creation_date'), blank=True)
    rating = models.FloatField(
        _('rating'),
        blank=True,
        validators=(MinValueValidator(0), MaxValueValidator(100)),
    )
    type = models.TextField(_('type'), choices=Type.choices)

    # Связи
    genres = models.ManyToManyField(Genre, through='GenreFilmwork')
    persons = models.ManyToManyField(Person, through='PersonFilmwork')

    def __str__(self):
        """Строковое представление модели.

        Returns:
            str: Название фильма
        """
        return self.title

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = _('filmwork')
        verbose_name_plural = _('filmworks')


class GenreFilmwork(UUIDMixin):
    """Промежуточная таблица для связи жанров и кинопроизведений."""

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"genre_film_work'
        constraints = (
            models.UniqueConstraint(
                fields=('film_work', 'genre'),
                name='film_work_genre_idx',
            ),
        )


class PersonFilmwork(UUIDMixin):
    """Промежуточная таблица для связи персон и кинопроизведений."""

    class Role(models.TextChoices):
        ACTOR = ('ACTOR', _('actor'))
        WRITER = ('WRITER', _('writer'))
        DIRECTOR = ('DIRECTOR', _('director'))

    film_work = models.ForeignKey('Filmwork', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)
    role = models.TextField(_('role'), choices=Role.choices)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'content\".\"person_film_work'
        constraints = (
            models.UniqueConstraint(
                fields=('film_work', 'person', 'role'),
                name='film_work_person_idx',
            ),
        )
