# -*- coding: utf-8 -*-

import debug_toolbar

from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import logout_then_login

from rest_framework.documentation import include_docs_urls
from invites.views import InviteRegistrationView
from .decorators import https_required
from .views import RegistrationView, LegacyURLView, template_viewer, home, login


urlpatterns = [
    url(r'^docs/', include_docs_urls(title='JumpCut API v1', public=False)),
    url(r'^api/v1/', include('api.v1.urls')),

    url(
        regex=r'^$',
        view=home,
        name='home'
    ),
    url(r'^films/', include('films.urls')),
    url(r'^forums/', include('forums.urls')),
    url(r'^invites/', include('invites.urls')),
    url(r'^users/', include('users.urls')),
    url(r'^torrent-requests/', include('torrent_requests.urls')),
    url(r'^torrent-stats/', include('torrent_stats.urls')),
    url(r'^torrents/', include('torrents.urls')),
    url(r'^wiki/', include('wiki.urls')),

    # Admin
    url(r'^grappelli/', include('grappelli.urls')),
    url(r'^admin/', admin.site.urls),

    # Registration
    url(
        regex=r'^register/$',
        view=RegistrationView.as_view(),
        name='open_registration',
    ),
    url(
        regex=r'^register/(?P<invite_key>[0-9a-f\-]{36})/$',
        view=InviteRegistrationView.as_view(),
        name='invite_registration',
    ),

    # Authentication
    url(
        regex=r'^login/$',
        view=https_required(login),
        name='login',
    ),
    url(
        regex=r'^logout/$',
        view=logout_then_login,
        name='logout',
    ),
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
