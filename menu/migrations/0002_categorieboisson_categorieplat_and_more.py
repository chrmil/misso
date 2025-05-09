# Generated by Django 5.1.7 on 2025-04-01 08:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="CategorieBoisson",
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
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name="CategoriePlat",
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
                ("description", models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.RemoveField(
            model_name="menuitem",
            name="category",
        ),
        migrations.RenameField(
            model_name="restaurant",
            old_name="location",
            new_name="emplacement",
        ),
        migrations.RenameField(
            model_name="restaurant",
            old_name="name",
            new_name="nom",
        ),
        migrations.CreateModel(
            name="Menu",
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
                (
                    "restaurant",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="menu.restaurant",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Boisson",
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
                (
                    "prixVerre",
                    models.DecimalField(decimal_places=2, max_digits=6, null=True),
                ),
                (
                    "prixBouteille",
                    models.DecimalField(decimal_places=2, max_digits=6, null=True),
                ),
                ("description", models.TextField(blank=True, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "categorie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="menu.categorieboisson",
                    ),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.menu"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Plat",
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
                ("prix", models.DecimalField(decimal_places=2, max_digits=6)),
                ("description", models.TextField(blank=True, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "categorie",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="menu.categorieplat",
                    ),
                ),
                (
                    "menu",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.menu"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AccompagnementPlat",
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
                ("prix", models.DecimalField(decimal_places=2, max_digits=6)),
                ("description", models.TextField(blank=True, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "plat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.plat"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="AccompagnementBoisson",
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
                ("prix", models.DecimalField(decimal_places=2, max_digits=6)),
                ("description", models.TextField(blank=True, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "plat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.plat"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VarianteBoisson",
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
                ("prix", models.DecimalField(decimal_places=2, max_digits=6)),
                ("description", models.TextField(blank=True, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "plat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.plat"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="VariantePlat",
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
                ("prix", models.DecimalField(decimal_places=2, max_digits=6)),
                ("description", models.TextField(blank=True, null=True)),
                ("image_path", models.CharField(blank=True, max_length=255, null=True)),
                (
                    "plat",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="menu.plat"
                    ),
                ),
            ],
        ),
        migrations.DeleteModel(
            name="Category",
        ),
        migrations.DeleteModel(
            name="MenuItem",
        ),
    ]
