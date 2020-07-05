from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import TestCase

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Post

from blog.serializers import PostSerializer
# import json

MY_POSTS_URL = reverse('blog:my_post-list')
POSTS_URL = reverse('blog:post-list')


class PublicMyPostApiTests(TestCase):
    """Test the publicly available Posts API"""

    def setUp(self):
        self.client = APIClient()

    def test_login_required(self):
        """Test that login is required to access the endpoint"""
        res = self.client.get(MY_POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateMyPostsApiTests(TestCase):
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

        res = self.client.get(MY_POSTS_URL)

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
                            author=user2)

        post = Post.objects.create(title='here comes dh',
                                   author=self.user)
        res = self.client.get(MY_POSTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        # print(json.dumps(res.data, indent=0))
        self.assertEqual(res.data[0]['title'], post.title)


class PublicPostApiTests(TestCase):
    """Test public Posts Apis"""

    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            'test1@experiment.com',
            'experiment'
        )
        self.user2 = get_user_model().objects.create_user(
            'test2@experiment.com',
            'experiment'
        )
        self.user3 = get_user_model().objects.create_user(
            'test3@experiment.com',
            'experiment'
        )
        Post.objects.create(title='Muh foodboy1',
                            author=self.user1)
        Post.objects.create(title='Muh foodboy2',
                            author=self.user2)
        Post.objects.create(title='Muh foodboy3',
                            author=self.user3)
        Post.objects.create(title='Muh foodboy4',
                            author=self.user2)
        Post.objects.create(title='Muh foodboy5',
                            author=self.user3)
        Post.objects.create(title='Muh foodboy6',
                            author=self.user1)
        self.client.force_authenticate(self.user1)

    def test_retreive_all_posts(self):
        """Test that all the posts are getting retreived"""
        res = self.client.get(POSTS_URL)

        posts = Post.objects.all().order_by('-title')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 6)
        self.assertEqual(res.data[0]['title'], posts[0].title)
