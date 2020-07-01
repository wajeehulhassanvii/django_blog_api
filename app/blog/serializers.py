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
    class Meta:
        model = Post
        fields = ('id', 'title')
        ordering = ('-publish')
        read_only_fields = ('id',)
