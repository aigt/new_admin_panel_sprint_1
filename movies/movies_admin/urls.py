"""URL Configuration."""
from django.contrib import admin
from django.urls import include, path

from movies_admin import settings

urlpatterns = [
    path('admin/', admin.site.urls),
]


if settings.DEBUG:  # pragma: no cover
    import debug_toolbar  # noqa: WPS433

    urlpatterns = [
        # URLs specific only to django-debug-toolbar:
        path('__debug__/', include(debug_toolbar.urls)),
        *urlpatterns,
    ]
