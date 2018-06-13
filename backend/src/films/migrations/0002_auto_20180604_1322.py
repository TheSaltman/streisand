# Generated by Django 2.0.6 on 2018-06-04 13:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('imdb', '0001_initial'),
        ('rotten_tomatoes', '0001_initial'),
        ('films', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='filmcomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='filmcomments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='filmcomment',
            name='film',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='films.Film'),
        ),
        migrations.AddField(
            model_name='film',
            name='imdb',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='imdb.FilmIMDb'),
        ),
        migrations.AddField(
            model_name='film',
            name='rotten_tomatoes',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='rotten_tomatoes.FilmRottenTomatoes'),
        ),
        migrations.AddField(
            model_name='film',
            name='tags',
            field=models.ManyToManyField(blank=True, related_name='films', to='films.Tag'),
        ),
        migrations.AddField(
            model_name='collectioncomment',
            name='author',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collectioncomments', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collectioncomment',
            name='collection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='films.Collection'),
        ),
        migrations.AddField(
            model_name='collection',
            name='collection_tags',
            field=models.ManyToManyField(related_name='collections', to='films.Tag'),
        ),
        migrations.AddField(
            model_name='collection',
            name='creator',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='collection_creators', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='film',
            field=models.ManyToManyField(related_name='lists', to='films.Film'),
        ),
    ]