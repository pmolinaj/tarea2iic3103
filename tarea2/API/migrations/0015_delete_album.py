# Generated by Django 3.2 on 2021-05-03 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0014_rename_artist_album_artist_id'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Album',
        ),
    ]
