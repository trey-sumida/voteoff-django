# Generated by Django 3.0.6 on 2020-05-21 00:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lists', '0005_allowedusers'),
    ]

    operations = [
        migrations.CreateModel(
            name='LastVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_voted', models.DateTimeField()),
                ('contest', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lists.Contest')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
