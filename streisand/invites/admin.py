# -*- coding: utf-8 -*-

from django.contrib import admin
from django.utils.timezone import now

from .models import Invite


class InviteAdmin(admin.ModelAdmin):

    ordering = ['-created_at']

    fields = (
        'key',
        'owner_profile_link',
        'created_at',
        'valid_until',
        'is_valid',
    )

    readonly_fields = fields

    list_display = fields

    search_fields = (
        'key',
        'owner__user__username',
        'owner__user__email',
    )

    def get_queryset(self, request):
        queryset = super(InviteAdmin, self).get_queryset(request)
        return queryset.select_related('owner__user')

    def owner_profile_link(self, invite):
        return '<a href="{profile_url}">{username}</a>'.format(
            profile_url=invite.owner.get_absolute_url(),
            username=invite.owner.username,
        )
    owner_profile_link.allow_tags = True

    def valid_until(self, invite):
        return invite.created_at + Invite.objects.INVITES_VALID_FOR

    def is_valid(self, invite):
        return invite.created_at < now() < self.valid_until(invite)


admin.site.register(Invite, InviteAdmin)
