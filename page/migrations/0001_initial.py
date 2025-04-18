# Generated by Django 5.1.7 on 2025-04-04 14:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Page",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100, unique=True)),
                ("emplacement", models.URLField(blank=True, max_length=500, null=True)),
                ("titre", models.TextField(blank=True, max_length=500, null=True)),
                ("sous_titre", models.TextField(blank=True, max_length=500, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Paragraphe",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100, unique=True)),
                ("titre", models.TextField(blank=True, max_length=500, null=True)),
                ("sous_titre", models.TextField(blank=True, max_length=500, null=True)),
                ("texte", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100, unique=True)),
                ("image_path", models.CharField(blank=True, max_length=300, null=True)),
                (
                    "paragraphe",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="page.paragraphe",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Section",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("nom", models.CharField(max_length=100, unique=True)),
                ("titre", models.TextField(blank=True, max_length=500, null=True)),
                ("sous_titre", models.TextField(blank=True, max_length=500, null=True)),
                ("visible", models.BooleanField(default=True)),
                (
                    "page",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="page.page"
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="paragraphe",
            name="section",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="page.section"
            ),
        ),
    ]
