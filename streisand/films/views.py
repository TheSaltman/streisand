# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet

from django.shortcuts import render, get_object_or_404

from www.utils import paginate

from .models import Film, Collection
from .serializers import AdminFilmSerializer, CollectionSerializer


class CollectionViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = CollectionSerializer
    queryset = Collection.objects.all().select_related(
        'creator',
    ).prefetch_related(
        'collection_tags',
    ).order_by(
        '-id',
    )

    def get_queryset(self):

        queryset = super().get_queryset()

        # Tag filtering
        if 'collection_tags' in self.request.query_params:
            queryset = queryset.filter(collection_tags__name=self.request.query_params['collection_tags'])

        return queryset


class FilmViewSet(ModelViewSet):
    """
    API endpoint that allows films to be viewed or edited.
    """
    permission_classes = [IsAdminUser]
    queryset = Film.objects.all().select_related(
        'imdb',
    ).prefetch_related(
        'tags',
    ).order_by(
        '-id',
    )
    serializer_class = AdminFilmSerializer

    def get_queryset(self):

        queryset = super().get_queryset()

        # Tag filtering
        if 'tag' in self.request.query_params:
            queryset = queryset.filter(tags__name=self.request.query_params['tag'])

        return queryset


def film_index(request):

    films = paginate(
        request=request,
        queryset=Film.objects.all(),
    )

    return render(
        request=request,
        template_name='film_index.html',
        context={
            'films': films,
        }
    )


def film_details(request, film_id, torrent_id=None):

    film = get_object_or_404(Film, id=film_id)

    if torrent_id is not None:
        torrent_id = int(torrent_id)

    torrents = film.torrents.select_related('moderated_by', 'uploaded_by')
    comments = film.comments.select_related('author')

    return render(
        request=request,
        template_name='film_details.html',
        context={
            'film': film,
            'torrent_id': torrent_id,
            'torrents': torrents,
            'comments': comments,
        }
    )
