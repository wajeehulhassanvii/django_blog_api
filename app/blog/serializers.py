from rest_framework import serializers

from core.models import Tag, Post


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'name')
        read_only_fields = ('id',)


class PostSerializer(serializers.ModelSerializer):
    """Serializer for Post"""
    # changed = serializers.DateTimeField(read_only=True)
    # updated = serializers.DateTimeField(read_only=True)
    # publish = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'title', 'body')
        ordering = ('-publish')
        read_only_fields = ('id',)
