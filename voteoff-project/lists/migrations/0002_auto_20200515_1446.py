# Generated by Django 3.0.6 on 2020-05-16 00:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lists', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contest',
            name='contest_image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='contest',
            name='contest_description',
            field=models.TextField(default='', max_length=300),
        ),
    ]
