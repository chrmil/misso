# Generated by Django 5.1.7 on 2025-04-03 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0007_utilisateur_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='utilisateur',
            name='niveau',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
