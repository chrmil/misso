# Generated by Django 4.2.20 on 2025-04-06 13:05

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MonModele',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=255)),
                ('date_creation', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
