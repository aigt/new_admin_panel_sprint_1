"""Настройки администраторской панели."""

from django.contrib import admin

from movies_admin.apps.movies import models

TIMESTAMP_FIELDS = (
    'created',
    'modified',
)


@admin.register(models.Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для жанров."""

    fields = (
        'name',
        'description',
        *TIMESTAMP_FIELDS,
    )
    readonly_fields = TIMESTAMP_FIELDS

    list_display = (
        'name',
        'description',
    )
    search_fields = ('name', 'description', 'id')


@admin.register(models.Person)
class PersonAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для персон."""

    fields = (
        'full_name',
        *TIMESTAMP_FIELDS,
    )
    readonly_fields = TIMESTAMP_FIELDS

    search_fields = ('full_name', 'id')


class GenreFilmworkInline(admin.TabularInline):
    """Настройки вложенной формы связи жанры-кинопроизведения."""

    model = models.GenreFilmwork
    fields = ('genre',)
    raw_id_fields = ('genre',)


class PersonFilmworkInline(admin.TabularInline):
    """Настройки вложенной формы связи персоны-кинопроизведения."""

    model = models.PersonFilmwork
    raw_id_fields = ('person',)


@admin.register(models.Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для кинопроизведений."""

    inlines = (
        GenreFilmworkInline,
        PersonFilmworkInline,
    )
    fields = (
        'title',
        'description',
        'creation_date',
        'rating',
        'type',
        *TIMESTAMP_FIELDS,
    )
    readonly_fields = TIMESTAMP_FIELDS

    list_display = (
        'title',
        'type',
        'creation_date',
        'rating',
    )
    list_filter = ('type',)
    search_fields = ('title', 'description', 'id')
