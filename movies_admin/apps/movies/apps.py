"""Настройки приложения."""
from django.apps import AppConfig


class MoviesConfig(AppConfig):
    """Конфиг приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies_admin.apps.movies'
