from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Tag

from blog import serializers


class TagViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
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
