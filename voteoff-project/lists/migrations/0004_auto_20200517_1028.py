# Generated by Django 3.0.6 on 2020-05-17 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0003_auto_20200516_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contest',
            name='end_date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='contest',
            name='start_date',
            field=models.DateTimeField(),
        ),
    ]
