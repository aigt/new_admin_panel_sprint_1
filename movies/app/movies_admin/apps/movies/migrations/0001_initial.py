import uuid

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models
from movies_admin import settings

DB_DDL_SCHEMA_FILE = settings.BASE_DIR.joinpath(
    'schema_design/movies_database.ddl',
)


def get_db_schema_query():
    with open(
        DB_DDL_SCHEMA_FILE,
        encoding='utf-8',
    ) as schema_file:
        db_schema_query = schema_file.read()
    return db_schema_query


class Migration(migrations.Migration):
    """Стартовые миграции."""

    initial = True

    dependencies = []

    database_operations = [
        migrations.RunSQL(
            sql=get_db_schema_query(),
            reverse_sql='DROP SCHEMA IF EXISTS content CASCADE;',
        ),
    ]

    state_operations = [
        migrations.CreateModel(
            name='Filmwork',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'title',
                    models.CharField(
                        max_length=255,
                        verbose_name='title',
                    ),
                ),
                (
                    'description',
                    models.TextField(blank=True, verbose_name='description'),
                ),
                (
                    'creation_date',
                    models.DateField(blank=True, verbose_name='creation_date'),
                ),
                (
                    'rating',
                    models.FloatField(
                        blank=True,
                        validators=[
                            django.core.validators.MinValueValidator(0),
                            django.core.validators.MaxValueValidator(100),
                        ],
                        verbose_name='rating',
                    ),
                ),
                (
                    'type',
                    models.TextField(
                        choices=[('MOVIE', 'movie'), ('TV_SHOW', 'tv_show')],
                        verbose_name='type',
                    ),
                ),
            ],
            options={
                'verbose_name': 'filmwork',
                'verbose_name_plural': 'filmworks',
                'db_table': 'content"."film_work',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'name',
                    models.CharField(
                        max_length=255,
                        verbose_name='name',
                    ),
                ),
                (
                    'description',
                    models.TextField(blank=True, verbose_name='description'),
                ),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'content"."genre',
            },
        ),
        migrations.CreateModel(
            name='Person',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                (
                    'full_name',
                    models.CharField(max_length=255, verbose_name='full_name'),
                ),
            ],
            options={
                'verbose_name': 'person',
                'verbose_name_plural': 'persons',
                'db_table': 'content"."person',
            },
        ),
        migrations.CreateModel(
            name='PersonFilmwork',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    'role',
                    models.TextField(
                        choices=[
                            ('ACTOR', 'actor'),
                            ('WRITER', 'writer'),
                            ('DIRECTOR', 'director'),
                        ],
                        verbose_name='role',
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                (
                    'film_work',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='movies.filmwork',
                    ),
                ),
                (
                    'person',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='movies.person',
                    ),
                ),
            ],
            options={
                'db_table': 'content"."person_film_work',
            },
        ),
        migrations.CreateModel(
            name='GenreFilmwork',
            fields=[
                (
                    'id',
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                ('created', models.DateTimeField(auto_now_add=True)),
                (
                    'film_work',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='movies.filmwork',
                    ),
                ),
                (
                    'genre',
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to='movies.genre',
                    ),
                ),
            ],
            options={
                'db_table': 'content"."genre_film_work',
            },
        ),
        migrations.AddField(
            model_name='filmwork',
            name='genres',
            field=models.ManyToManyField(
                through='movies.GenreFilmwork',
                to='movies.Genre',
            ),
        ),
        migrations.AddField(
            model_name='filmwork',
            name='persons',
            field=models.ManyToManyField(
                through='movies.PersonFilmwork',
                to='movies.Person',
            ),
        ),
        migrations.AddConstraint(
            model_name='personfilmwork',
            constraint=models.UniqueConstraint(
                fields=('film_work', 'person', 'role'),
                name='film_work_person_idx',
            ),
        ),
        migrations.AddConstraint(
            model_name='genrefilmwork',
            constraint=models.UniqueConstraint(
                fields=('film_work', 'genre'),
                name='film_work_genre_idx',
            ),
        ),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=database_operations,
            state_operations=state_operations,
        ),
    ]