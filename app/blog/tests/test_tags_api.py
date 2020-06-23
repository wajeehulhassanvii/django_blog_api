from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Tag

from blog.serializers import TagSerializer


# below url for listing tag
TAGS_URL = reverse('blog:tag-list')


class PublicTagsApiTests(TestCase):
    """Test the publicly available tags API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required for retrieving tags"""
        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateTagsApiTests(TestCase):
    """Test the authorized user tags API"""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            'test@experiment.com',
            'experiment'
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_tags(self):
        """Test retrieving tags"""
        Tag.objects.create(user=self.user, name='Scripture')
        Tag.objects.create(user=self.user, name='Dessert')

        res = self.client.get(TAGS_URL)

        tags = Tag.objects.all().order_by('-name')
        # since we will have more than one in serializer therefore many=True
        # we used many=True also so the serializer know that we serializing
        # a list and not a single object
        serializer = TagSerializer(tags, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_limited_to_user(self):
        """Test that tags returned are for an authenticated user"""
        user2 = get_user_model().objects.create_user(
            'other@experiment.com',
            'experiment'
        )
        Tag.objects.create(user=user2, name='Morality')
        tag = Tag.objects.create(user=self.user, name='Prayer')

        res = self.client.get(TAGS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['name'], tag.name)

    def test_create_tag_successful(self):
        """Test creating a new tag"""
        payload = {'name': 'Test tag'}
        self.client.post(TAGS_URL, payload)

        exists = Tag.objects.filter(user=self.user,
                                    name=payload['name']).exists()
        self.assertTrue(exists)

    def test_create_tag_with_invalid_tag(self):
        """Test creating a new invalid payload test"""
        payload = {'name': ''}
        res = self.client.post(TAGS_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
