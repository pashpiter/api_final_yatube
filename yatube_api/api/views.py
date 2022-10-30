from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import pagination, permissions, serializers, viewsets

from posts.models import Comment, Follow, Group, Post
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
        return Comment.objects.filter(post=post)

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)


class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        search = self.request.query_params.get('search')
        if self.request.query_params.get('search'):
            return self.request.user.follow.filter(following__username=search)
        return self.request.user.follow.all()

    def perform_create(self, serializer):
        if not serializer.initial_data.get('following'):
            raise serializers.ValidationError('111')
        follower = get_object_or_404(
            User, username=serializer.initial_data['following'])
        user = self.request.user
        if (user != follower) and not (Follow.objects.filter(
                                       user=user, following=follower)):
            return serializer.save(user=user, following=follower)
        raise serializers.ValidationError('На себя нельзя подписаться')
