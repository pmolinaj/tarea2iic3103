# Generated by Django 3.2 on 2021-05-02 21:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('API', '0002_auto_20210501_1938'),
    ]

    operations = [
        migrations.AddField(
            model_name='artista',
            name='self_url',
            field=models.CharField(default=True, max_length=200),
        ),
    ]
