# Generated by Django 3.2 on 2021-05-03 03:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0005_auto_20210502_2232'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='artista',
            name='albums',
        ),
        migrations.RemoveField(
            model_name='artista',
            name='self_url',
        ),
        migrations.RemoveField(
            model_name='artista',
            name='tracks',
        ),
    ]
