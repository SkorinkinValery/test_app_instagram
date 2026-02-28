from rest_framework import serializers
from instagram.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        post_id = validated_data.pop('id')

        post, created = Post.objects.update_or_create(id=post_id, defaults=validated_data)
        return post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        comment_id = validated_data.pop('id')

        comment, created = Comment.objects.update_or_create(id=comment_id, defaults=validated_data)
        return comment