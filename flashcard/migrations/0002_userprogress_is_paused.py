# Generated by Django 5.1 on 2024-09-16 05:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('flashcard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprogress',
            name='is_paused',
            field=models.BooleanField(default=False),
        ),
    ]
