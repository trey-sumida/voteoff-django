# Generated by Django 3.0.6 on 2020-05-11 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='public',
            field=models.BooleanField(default=False),
        ),
    ]
