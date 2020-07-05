from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag, Post

from blog import serializers


class TagViewSet(viewsets.GenericViewSet,
                 mixins.ListModelMixin,
                 mixins.CreateModelMixin):
    """Manage tags in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Tag.objects.all()
    serializer_class = serializers.TagSerializer

    # the get_queryset function is called when viewset (list func) is
    # invoked, it will call get_queryset to retrieve these objects
    # here we customize any query
    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        # below we are getting authenticated user
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self, serializer):
        """Create a new tag"""
        serializer.save(user=self.request.user)


class MyPostViewSet(viewsets.GenericViewSet,
                    mixins.ListModelMixin,
                    mixins.CreateModelMixin):
    """Manage Post in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        """Return objects for the current authenticated user only"""
        return self.queryset.\
            filter(author=self.request.user).order_by('-title')

    def perform_create(self):
        """perform create for Post object
        Keyword arguments:
        Return: return_description
        """
        serializers.save(user=self.request.user)


class PostViewSet(viewsets.GenericViewSet,
                  mixins.ListModelMixin):
    """Manage Post in the database for public"""
    queryset = Post.objects.all()
    serializer_class = serializers.PostSerializer

    def get_queryset(self):
        """Return objects for the public users"""
        return self.queryset.order_by('-title')
