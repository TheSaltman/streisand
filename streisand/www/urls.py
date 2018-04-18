# -*- coding: utf-8 -*-

import debug_toolbar

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin

from rest_framework.documentation import include_docs_urls
from .views import LegacyURLView, template_viewer


urlpatterns = [
    url(r'^api/v1/', include('interfaces.api_site.urls')),
    url(r'^docs/', include_docs_urls(title='JumpCut API v1', public=False)),
    url(r'^model-docs/', include('docs.urls')),
    url(r'^films/', include('films.urls')),
    url(r'^forums/', include('forums.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^torrent-requests/', include('torrent_requests.urls')),
    url(r'^torrent-stats/', include('torrent_stats.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^wiki/', include('wiki.urls')),

    # Admin
    url(r'^admin/', admin.site.urls),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),


    # Authentication
    url(r'^su/', include('django_su.urls')),

    # Utils
    url(
        regex=r'^templates/(?P<template_path>.*\.html)$',
        view=template_viewer,
        name='template_viewer',
    ),

    # Legacy
    url(
        regex=r'^(?P<section>.+)\.php$',
        view=LegacyURLView.as_view(),
        name='legacy_url',
    ),
]

if settings.DEBUG:
    urlpatterns.append(
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
