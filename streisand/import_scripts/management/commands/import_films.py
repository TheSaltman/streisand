# -*- coding: utf-8 -*-

from import_scripts.management.commands import MySQLCommand

from films.models import Film


class Command(MySQLCommand):

    SQL = """SELECT * FROM torrents_group LIMIT 100"""

    help = "Imports films from the MySQL db"

    @staticmethod
    def handle_row(row):

        tags = row['TagList'].strip('|').split('|')

        title = row['Name'].encode('latin-1').decode('utf-8')
        description = row['WikiBody'].encode('latin-1').decode('utf-8')
        notes = row['DoTNotes'].encode('latin-1').decode('utf-8')

        yt_id = row['YouTube']
        imdb_id = row['IMDB']

        film_id = row['ID']
        if film_id == 14457 or film_id == 14458:
            imdb_id = None

        f = Film.objects.create(
            old_id=film_id,
            title=title,
            year=row['Year'],
            imdb_id=imdb_id,
            description=description,
            moderation_notes=notes,
            poster_url=row['WikiImage'],
            trailer_url='https://www.youtube.com/watch?v={id}'.format(id=yt_id) if yt_id else '',
        )

        f.tags = tags

        print(f.old_id)