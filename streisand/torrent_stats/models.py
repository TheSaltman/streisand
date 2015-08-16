# -*- coding: utf-8 -*-

from uuid import uuid4

from django.db import models
from django.utils.timezone import timedelta


class TorrentStats(models.Model):

    # Because Django does not support compound primary keys, and because this
    # table might actually hit the max limit of an auto-incrementing integer ID,
    # we use an auto-generated UUIDField as the primary key.
    id = models.UUIDField(default=uuid4, primary_key=True, editable=False)

    profile = models.ForeignKey(
        'profiles.UserProfile',
        null=False,
        related_name='torrent_stats',
    )
    torrent = models.ForeignKey(
        'torrents.Torrent',
        null=False,
        related_name='torrent_stats',
    )

    bytes_uploaded = models.BigIntegerField(default=0)
    bytes_downloaded = models.BigIntegerField(default=0)

    first_snatched = models.DateTimeField(null=True)
    last_snatched = models.DateTimeField(null=True, db_index=True)
    snatch_count = models.IntegerField(default=0, db_index=True)

    last_seeded = models.DateTimeField(null=True)
    seed_time = models.DurationField(default=timedelta(minutes=0))

    hnr_countdown_started_at = models.DateTimeField(null=True)
    is_hit_and_run = models.NullBooleanField()

    class Meta:
        unique_together = ['profile', 'torrent']
        index_together = ['profile', 'torrent']

    def __str__(self):
        return 'Torrent stats for {user} on {torrent}'.format(
            user=self.profile,
            torrent=self.torrent,
        )

    @property
    def seed_time_remaining(self):
        return timedelta(hours=96) - self.seed_time