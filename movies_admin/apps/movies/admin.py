from django.contrib import admin

from .models import Genre


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
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
