# Generated by Django 2.0.4 on 2018-05-04 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.PositiveIntegerField(db_index=True, null=True)),
                ('sort_order', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=256)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='forums.ForumGroup')),
            ],
            options={
                'ordering': ['sort_order'],
            },
        ),
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.PositiveIntegerField(db_index=True, null=True)),
                ('body', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified', models.BooleanField(default=False)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('author', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='forum_posts', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_posts', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'created_at',
            },
        ),
        migrations.CreateModel(
            name='ForumReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reported_at', models.DateTimeField(auto_now_add=True)),
                ('reason', models.TextField(max_length=1024)),
                ('resolved', models.BooleanField(default=False)),
                ('date_resolved', models.DateTimeField(blank=True, null=True)),
                ('post', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='forums.ForumPost')),
                ('reporting_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='reports', to=settings.AUTH_USER_MODEL)),
                ('resolved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='report_resolved', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-reported_at',),
            },
        ),
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.PositiveIntegerField(db_index=True, null=True)),
                ('title', models.CharField(max_length=1024)),
                ('is_locked', models.BooleanField(default=False)),
                ('is_sticky', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('modified', models.BooleanField(default=False)),
                ('modified_at', models.DateTimeField(auto_now=True, null=True)),
                ('modified_count', models.PositiveIntegerField(default=0, editable=False)),
                ('number_of_posts', models.PositiveIntegerField(default=0)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='forum_threads_created', to=settings.AUTH_USER_MODEL)),
                ('latest_post', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='thread_latest', to='forums.ForumPost')),
                ('modified_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='modified_threads', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': '-created_at',
            },
        ),
        migrations.CreateModel(
            name='ForumThreadSubscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('thread', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscriptions', to='forums.ForumThread')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='forum_thread_subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ForumTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('old_id', models.PositiveIntegerField(db_index=True, null=True)),
                ('sort_order', models.PositiveSmallIntegerField()),
                ('name', models.CharField(max_length=256)),
                ('description', models.CharField(max_length=1024)),
                ('is_archived', models.BooleanField(default=False)),
                ('staff_only_thread_creation', models.BooleanField(default=False)),
                ('last_active', models.DateTimeField(blank=True, default=django.utils.timezone.now, editable=False)),
                ('number_of_threads', models.PositiveIntegerField(default=0)),
                ('number_of_posts', models.PositiveIntegerField(default=0)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='topics', to='forums.ForumGroup')),
                ('latest_post', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='topic_latest', to='forums.ForumPost')),
                ('minimum_user_class', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='unlocked_forum_topics', to='users.UserClass')),
            ],
            options={
                'ordering': ['sort_order'],
            },
        ),
        migrations.AddField(
            model_name='forumthread',
            name='subscribed_users',
            field=models.ManyToManyField(related_name='forum_threads_subscribed', through='forums.ForumThreadSubscription', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='forumthread',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='threads', to='forums.ForumTopic'),
        ),
        migrations.AddField(
            model_name='forumreport',
            name='thread',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='forums.ForumThread'),
        ),
        migrations.AddField(
            model_name='forumpost',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='forums.ForumThread'),
        ),
    ]
