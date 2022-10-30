from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import pagination, permissions, viewsets, filters, mixins

from posts.models import Follow, Group, Post
from .permissions import IsAuthorOrReadOnly
from .serializers import (CommentSerializer, FollowSerializer, GroupSerializer,
                          PostSerializer)

User = get_user_model()


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    pagination_class = pagination.LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments.all()

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowGetPostViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                           viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ['following__username']

    def get_queryset(self):
        return self.request.user.follow.all()

    def perform_create(self, serializer):
        # if not serializer.initial_data.get('following'):
        #     raise serializers.ValidationError('111')
        follower = get_object_or_404(
            User, username=self.request.data['following'])
        # user = self.request.user
        # if (user != follower) and not (Follow.objects.filter(
        #                                user=user, following=follower)):
        #     return serializer.save(user=user, following=follower)
        # raise serializers.ValidationError('На себя нельзя подписаться')
        serializer.save(user=self.request.user, following=follower)
