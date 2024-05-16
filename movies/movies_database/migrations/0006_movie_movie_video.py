# Generated by Django 4.2.5 on 2024-05-13 09:13

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_database', '0005_profession_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movie_video',
            field=models.FileField(blank=True, null=True, upload_to='video/<django.db.models.fields.CharField>/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['mp4'])]),
        ),
    ]
