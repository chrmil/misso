# Generated by Django 5.1.7 on 2025-04-06 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0009_restaurant_image_path"),
    ]

    operations = [
        migrations.AddField(
            model_name="accompagnementboisson",
            name="priorite",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="accompagnementplat",
            name="priorite",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="boisson",
            name="priorite",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="categorieboisson",
            name="priorite",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="categorieplat",
            name="priorite",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="menu",
            name="priorite",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="plat",
            name="priorite",
            field=models.PositiveIntegerField(default=0),
        ),
    ]
