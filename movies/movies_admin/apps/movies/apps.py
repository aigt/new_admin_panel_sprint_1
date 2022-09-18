"""Настройки приложения."""
from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MoviesConfig(AppConfig):
    """Конфиг приложения."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'movies_admin.apps.movies'

    verbose_name = _('movies')
