# -*- coding: utf-8 -*-

from django.contrib.auth.decorators import permission_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views.generic import View

from profiles.models import UserProfile

from .models import Torrent, ReseedRequest
from .forms import TorrentUploadForm


class TorrentDownloadView(View):

    def get(self, request, torrent_id, announce_key):

        # Make sure we have a valid announce key
        try:
            profile = UserProfile.objects.get(announce_key_id=announce_key)
        except UserProfile.DoesNotExist:
            raise PermissionDenied

        # Make sure the user can download torrents
        if not profile.user.has_perm('torrents.can_download'):
            raise PermissionDenied

        # Make sure we have a valid torrent id
        torrent = get_object_or_404(
            Torrent.objects.select_related('metainfo'),
            id=torrent_id,
        )

        # Respond with the customized torrent
        response = HttpResponse(
            content=torrent.metainfo.for_user_download(profile),
            content_type='application/x-bittorrent',
        )
        response['Content-Disposition'] = 'attachment; filename={release_name}.torrent'.format(
            release_name=torrent.release_name,
        )
        return response


class TorrentUploadView(View):

    def get(self, request):

        torrent_upload_form = TorrentUploadForm(uploader_profile=request.user.profile)
        return self._render(torrent_upload_form)

    @method_decorator(permission_required('torrents.can_upload', raise_exception=True))
    def post(self, request):

        torrent_upload_form = TorrentUploadForm(
            request.POST,
            request.FILES,
            uploader_profile=request.user.profile,
        )

        if torrent_upload_form.is_valid():

            # Save the new Torrent object
            try:
                new_torrent = torrent_upload_form.save()
            except IntegrityError as e:
                if 'unique' in str(e):
                    torrent_upload_form.add_error('torrent_file', 'That torrent has already been uploaded')
                else:
                    raise
            else:
                return redirect(new_torrent)

        # Render the form with errors
        return self._render(torrent_upload_form)

    def _render(self, form):
        """
        Render the page with the given form.
        """
        return render(
            request=self.request,
            template_name='torrent_upload.html',
            dictionary={'form': form},
        )


class TorrentModerationView(View):

    @method_decorator(permission_required('torrents.can_moderate', raise_exception=True))
    def post(self, request, torrent_id):

        torrent = get_object_or_404(Torrent, id=torrent_id)

        moderation_status = request.POST['moderation_status']

        if moderation_status == 'approved':
            torrent.is_approved = True
        elif moderation_status == 'needs_work':
            torrent.is_approved = False
        else:
            torrent.is_approved = None

        torrent.moderated_by = request.user.profile
        torrent.save()

        return redirect(torrent)


def reseed_request_index(request):

    all_reseed_requests = ReseedRequest.objects.filter(
        active_on_torrent__isnull=False,
    ).select_related(
        'created_by__user',
        'torrent',
    ).order_by(
        '-created_at',
    )

    # Show 50 requests per page
    paginator = Paginator(all_reseed_requests, 50)

    page = request.GET.get('page')
    try:
        reseed_requests = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        reseed_requests = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        reseed_requests = paginator.page(paginator.num_pages)

    return render(
        request=request,
        template_name='reseed_request_index.html',
        dictionary={
            'reseed_requests': reseed_requests,
        }
    )


@permission_required('torrents.can_request_reseed', raise_exception=True)
def new_reseed_request(request, torrent_id):

    torrent = get_object_or_404(Torrent, id=torrent_id)

    if not torrent.is_accepting_reseed_requests:
        raise PermissionDenied

    torrent.request_reseed(request.user.profile)

    return redirect(torrent)
