# -*- coding: utf-8 -*-

from rest_framework.permissions import IsAdminUser
from rest_framework.viewsets import ModelViewSet
from collections import OrderedDict

from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View

from www.utils import paginate

from .forms import ForumPostForm
from .models import ForumGroup, ForumTopic, ForumThread, ForumPost
from .serializers import (
    ForumGroupSerializer,
    ForumTopicSerializer,
    ForumThreadSerializer,
    ForumPostSerializer,
)


class ForumGroupViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = ForumGroupSerializer
    queryset = ForumGroup.objects.all().prefetch_related(
        'topics__latest_post__author__user',
        'topics__latest_post__author__user_class',
        'topics__latest_post__thread',
    )


class ForumTopicViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = ForumTopicSerializer
    queryset = ForumTopic.objects.all().select_related(
        'group',
        'minimum_user_class',
        'latest_post__author__user',
        'latest_post__author__user_class',
        'latest_post__thread',
    ).prefetch_related(
        'threads__created_by__user',
        'threads__latest_post__author__user',
        'threads__latest_post__author__user_class',
        'threads__latest_post__thread',
    )

    def get_queryset(self):

        queryset = super().get_queryset()

        group_id = self.request.query_params.get('group_id', None)
        if group_id is not None:
            queryset = queryset.filter(group_id=group_id)

        return queryset


class ForumThreadViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = ForumThreadSerializer
    queryset = ForumThread.objects.all().select_related(
        'latest_post__author__user',
        'latest_post__author__user_class',
        'latest_post__thread',
    ).prefetch_related(
        'posts__author__user',
        'posts__author__user_class',
    )

    def get_queryset(self):

        queryset = super().get_queryset()

        topic_id = self.request.query_params.get('topic_id', None)
        if topic_id is not None:
            queryset = queryset.filter(topic_id=topic_id)

        return queryset


class ForumPostViewSet(ModelViewSet):

    permission_classes = [IsAdminUser]
    serializer_class = ForumPostSerializer
    queryset = ForumPost.objects.all().select_related(
        'thread',
        'author__user',
        'author__user_class',
    )

    def get_queryset(self):

        queryset = super().get_queryset()

        thread_id = self.request.query_params.get('thread_id', None)
        if thread_id is not None:
            queryset = queryset.filter(thread_id=thread_id)

        return queryset


def forum_index(request):

    forum_topics = ForumTopic.objects.accessible_to_user(request.user).select_related(
        'group',
    ).order_by(
        'group__sort_order',
        'sort_order',
    )

    forum_groups = OrderedDict()
    for topic in forum_topics:
        group_name = topic.group.name
        if group_name in forum_groups:
            forum_groups[group_name].append(topic)
        else:
            forum_groups[group_name] = [topic]

    return render(
        request=request,
        template_name='forum_index.html',
        context={
            'forum_groups': forum_groups,
        }
    )


def forum_topic_details(request, topic_id):

    topic = get_object_or_404(
        ForumTopic.objects.accessible_to_user(request.user),
        id=topic_id,
    )

    threads = paginate(
        request=request,
        queryset=topic.threads.select_related(
            'created_by__user',
        ),
        items_per_page=25,
    )

    return render(
        request=request,
        template_name='forum_topic_details.html',
        context={
            'topic': topic,
            'threads': threads,
        }
    )


def forum_post_delete(request, post_id):

    post = get_object_or_404(
        ForumPost,
        id=post_id
    )

    thread = post.thread

    post.delete()

    return redirect(thread)


class ForumThreadView(View):

    def dispatch(self, request, *args, **kwargs):

        self.thread = get_object_or_404(
            ForumThread.objects.accessible_to_user(request.user),
            id=kwargs.pop('thread_id'),
        )

        self.posts = paginate(
            request=request,
            queryset=self.thread.posts.select_related(
                'author__user',
            ),
            items_per_page=25,
        )

        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):

        form = ForumPostForm(
            thread=self.thread,
            author=request.user.profile,
        )

        return self._render(
            thread=self.thread,
            posts=self.posts,
            form=form,
        )

    def post(self, request):

        form = ForumPostForm(
            request.POST,
            thread=self.thread,
            author=request.user.profile,
        )

        if form.is_valid():

            forum_post = form.save()
            return redirect(forum_post)

        else:

            return self._render(
                thread=self.thread,
                posts=self.posts,
                form=form,
            )

    def _render(self, thread, posts, form):
        return render(
            request=self.request,
            template_name='forum_thread_details.html',
            context={
                'thread': thread,
                'posts': posts,
                'form': form,
            },
        )
