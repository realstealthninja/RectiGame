# Generated by Django 4.2.6 on 2024-05-24 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(blank=True, max_length=50, primary_key=True, serialize=False)),
                ('description', models.TextField(max_length=1000)),
                ('image', models.ImageField(upload_to='topic/images')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='topic/icons')),
                ('banner', models.ImageField(blank=True, null=True, upload_to='topic/banners')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='TopicTag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('slug', models.CharField(blank=True, max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='TopicMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nickname', models.CharField(blank=True, max_length=30, null=True)),
                ('permissions', models.PositiveBigIntegerField(default=127)),
                ('joined_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('has_left', models.BooleanField(default=False)),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_members', to='topics.topic')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='topic_member', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('topic', 'user')},
            },
        ),
        migrations.AddField(
            model_name='topic',
            name='tags',
            field=models.ManyToManyField(blank=True, to='topics.topictag'),
        ),
        migrations.CreateModel(
            name='CustomTopicEmoji',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('image', models.ImageField(upload_to='topic/custom_emojis')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='topics.topicmember')),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='topics.topic')),
            ],
        ),
    ]
