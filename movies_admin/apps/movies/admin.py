from django.contrib import admin

from movies_admin.apps.movies.models import Filmwork, Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для жанров."""

    fields = (
        'name',
        'description',
        'created',
        'modified',
    )
    readonly_fields = (
        'created',
        'modified',
    )


@admin.register(Filmwork)
class FilmworkAdmin(admin.ModelAdmin):
    """Настройки администраторской панели для кинопроизведений."""

    fields = (
        'title',
        'description',
        'creation_date',
        'rating',
        'type',
        'created',
        'modified',
    )
    readonly_fields = (
        'created',
        'modified',
    )
