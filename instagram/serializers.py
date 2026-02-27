from rest_framework import serializers
from instagram.models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

    def create(self, validated_data):
        id = validated_data.pop('id')

        post = Post.objects.update_or_create(id=id, defaults=validated_data)
        return post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'post', 'text', 'username', 'timestamp', 'ig_comment_id']
        read_only_fields = ['ig_comment_id', 'username', 'timestamp']