from django.contrib import admin

from movies_admin.apps.movies.models import Filmwork, Genre, GenreFilmwork

TIMESTAMP_FIELDS = (
    'created',
    'modified',
)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для жанров."""

    fields = (
        'name',
        'description',
        *TIMESTAMP_FIELDS,
    )
    readonly_fields = TIMESTAMP_FIELDS


class GenreFilmworkInline(admin.TabularInline):
    """Настройки вложенной формы связи жанры-кинопроизведения."""

    model = GenreFilmwork


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для кинопроизведений."""

    inlines = (GenreFilmworkInline,)
    fields = (
        'title',
        'description',
        'creation_date',
        'rating',
        'type',
        *TIMESTAMP_FIELDS,
    )
    readonly_fields = TIMESTAMP_FIELDS
