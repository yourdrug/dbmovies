# Generated by Django 4.2.5 on 2023-11-02 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies_database', '0004_alter_profession_movie_alter_profession_person'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profession',
            name='en_name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='profession',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]