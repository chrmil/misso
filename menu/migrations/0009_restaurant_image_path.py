# Generated by Django 5.1.7 on 2025-04-01 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("menu", "0008_restaurant_description_restaurant_titre"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurant",
            name="image_path",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
