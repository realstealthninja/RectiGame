# Generated by Django 4.1.1 on 2022-09-24 12:25

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('topics', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='topic',
            name='created_at',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]