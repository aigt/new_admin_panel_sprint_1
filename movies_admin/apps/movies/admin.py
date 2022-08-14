from django.contrib import admin

from movies_admin.apps.movies.models import Filmwork, Genre, GenreFilmwork


class TimeStampMixins:
    """Миксин с датами создания и модификации."""

    fields = (
        'created',
        'modified',
    )
    readonly_fields = (
        'created',
        'modified',
    )


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для жанров."""

    fields = (
        'name',
        'description',
        *TimeStampMixins.fields,
    )
    readonly_fields = TimeStampMixins.readonly_fields


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
        *TimeStampMixins.fields,
    )
    readonly_fields = TimeStampMixins.readonly_fields
