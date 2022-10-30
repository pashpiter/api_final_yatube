from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        model = Comment
        read_only_fields = ('post',)


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group


class FollowSerializer(serializers.ModelSerializer):
    user = SlugRelatedField(
        read_only=True, slug_field='username',
    )
    following = SlugRelatedField(
        read_only=True, slug_field='username'
    )

    def validate(self, data):
        if (data['user'] != data['following']) and not (
            Follow.objects.filter(user=self.request.user, following=data['following'])):
            return data
        raise serializers.ValidationError('На себя нельзя подписаться')

    class Meta:
        fields = '__all__'
        model = Follow
