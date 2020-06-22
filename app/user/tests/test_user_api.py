from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token')
ME_URL = reverse('user:me')


# anything we do multiple times we create helper function for that


def create_user(**params):
    return get_user_model().objects.create_user(**params)


# for better readability we seperate Public and Private APIs
class PublicUserApiTests(TestCase):
    """Test the users API (public)"""

    def setUp(self):
        self.client = APIClient()

        def test_create_valid_user_success(self):
            """Test creating user with valid payload is successful"""
            payload = {
                'email': 'test@experiment.com',
                'password': 'experiment',
                'first_name': 'Test name'
            }
            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_201_CREATED)
            user = get_user_model().objects.get(**res.data)
            self.assertTrue(user.check_password(payload['password']))
            self.assertNotIn('password', res.data)

        def test_user_exists(self):
            """Test creating user that already exists fails"""
            payload = {'email': 'test@experiment.com',
                       'password': 'experiment'}
            create_user(**payload)

            res = self.client.post(CREATE_USER_URL, payload)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_password_too_short(self):
            """Test that the password must be more than 5 characters"""
            payload = {'email': 'test@experiment.com', 'password': 'pw'}
            res = self.client.post(CREATE_USER_URL, payload)

            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            user_exists = get_user_model().objects.filter(
                email=payload['email']
            ).exists()
            self.assertFalse(user_exists)

        def test_create_token_for_user(self):
            """Test that the token is created for user"""
            payload = {
                'email': 'test@experiment.com',
                'password': 'experiment',
            }
            create_user(**payload)
            res = self.client.post(TOKEN_URL, payload)

            self.assertIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_200_OK)

        def test_token_invalid_credentials(self):
            """Test that token not created when credentials are inavlid"""
            create_user(email='test@experiment.com', password='testpass')
            payload = {
                'email': 'test@experiment.com',
                'password': 'pass'
            }
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_no_user(self):
            """Test that token is not created if user doesn't exist"""
            payload = {'email': 'test@experiment.com',
                       'password': 'testpass'}
            res = self.client.post(TOKEN_URL, payload)

            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_create_token_missing_field(self):
            """Test that email and password are required"""
            res = self.client.post(TOKEN_URL, {'email': 'one',
                                               'password': ''})
            self.assertNotIn('token', res.data)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        def test_retrieve_user_unauthorized(self):
            """Test that authentication is required for users"""
            res = self.client.get(ME_URL)

            self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication"""
    def setUp(self):
        self.user = create_user(
            email='test@experiment.com',
            password='testpass',
            first_name='first name'
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile logged in used"""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'first_name': self.user.first_name,
            'email': self.user.email
        })

    def test_post_me_not_allowed(self):
        """Test that post is not allowed on the me url"""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code,
                            status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for authorized user"""
        payload = {'first_name': 'new name', 'password': 'newpassword123'}

        res = self.client.patch(ME_URL, payload)
        self.assertEqual(self.user.first_name, payload['first_name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
