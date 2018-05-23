# Generated by Django 2.0.5 on 2018-05-21 03:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumtopic',
            name='is_archived',
        ),
        migrations.AddField(
            model_name='forumthread',
            name='is_archived',
            field=models.NullBooleanField(default=False),
        ),
    ]