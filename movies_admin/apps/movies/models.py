"""Модели прложения."""

import uuid

from django.db import models

GENRE_NAME_MAX_LENGTH = 255
FILMWORK_TITLE_MAX_LENGTH = 255


class Genre(models.Model):
    """Жанр."""

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField('name', max_length=GENRE_NAME_MAX_LENGTH)
    description = models.TextField('description', blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Строковое представление модели.

        Returns:
            str: Имя жанра
        """
        return self.name

    class Meta:
        db_table = 'content\".\"genre'
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Filmwork(models.Model):
    """Кинопроизведения."""

    class Type(models.TextChoices):
        MOVIE = ('MOVIE', 'movie')
        TV_SHOW = ('TV_SHOW', 'tv_show')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField('title', max_length=FILMWORK_TITLE_MAX_LENGTH)
    description = models.TextField('description', blank=True)
    creation_date = models.DateField('creation_date', blank=True)
    rating = models.FloatField('rating', blank=True)
    type = models.TextField('type', choices=Type.choices)
    created = models.DateTimeField(auto_now_add=True, blank=True)
    modified = models.DateTimeField(auto_now=True, blank=True)

    def __str__(self):
        """Строковое представление модели.

        Returns:
            str: Название фильма
        """
        return self.title

    class Meta:
        db_table = 'content\".\"film_work'
        verbose_name = 'Кинопроизведение'
        verbose_name_plural = 'Кинопроизведения'
