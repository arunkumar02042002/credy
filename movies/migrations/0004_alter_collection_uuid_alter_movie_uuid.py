# Generated by Django 5.1 on 2024-08-18 11:12

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0003_alter_movie_uuid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='uuid',
            field=models.UUIDField(db_index=True, default=uuid.uuid4, editable=False, unique=True),
        ),
        migrations.AlterField(
            model_name='movie',
            name='uuid',
            field=models.CharField(default=uuid.uuid4, max_length=100),
        ),
    ]
