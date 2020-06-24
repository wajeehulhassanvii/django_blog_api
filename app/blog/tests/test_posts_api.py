from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post
from blog.serializers import PostSerializer


POSTS_URL = reverse('blog:post-list')


class PublicPostApiTests(TestCase):
    """Test the publicly available Posts API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class PrivatePostsApiTests(TestCase):
    """Test private Post APIs"""

    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            'test@experiment.com',
            'experiment'
        )
        self.client.force_authenticate(self.user)

    def test_retrieve_posts_list_of_user(self):
        """Test retrieving list of Posts for authenticated user"""
        Post.objects.create(author=self.user,
                            title='Debunking AP\'s claim')
        Post.objects.create(author=self.user,
                            title='Sameer with another lie')

        res = self.client.get(POSTS_URL)

        posts = Post.objects.all().order_by('-title')
        serializer = PostSerializer(posts, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        self.assertEqual(res.data, serializer.data)

    def test_posts_limited_to_user(self):
        """Test that only posts for the authenticated user are returned"""
        user2 = get_user_model().objects.create_user(
            'other@experiment.com',
            'experiment'
        )
        Post.objects.create(title='Muh foodboy',
                            slug='one-more-post',
                            body='Muh foodboy.',
                            author=user2)

        post = Post.objects.create(title='here comes dh',
                                    slug='one-more-post',
                                    body='here comes dh',
                                    author=self.user)

        res = self.client.get(POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        self.assertEqual(res.data[0]['title'], post.title)
