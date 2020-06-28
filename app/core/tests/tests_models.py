from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


def sample_user(email='test@experiment.com', password='experiment'):
    """Create a sample user"""
    return get_user_model().objects.create_user(email, password)


class ModelTests(TestCase):

    def test_create_user_with_email_successful(self):
        """Test creating a new user with an email is successful"""
        email = 'test@experiment.com'
        password = 'experiment'
        user = get_user_model().objects.create_user(
            email=email,
            password=password
        )

        self.assertEqual(user.email, email)
        # check_password comes default with django user model,
        # returns true if password is correct
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test the email for the new user is normalized"""
        email = 'test@experiment.com'
        user = get_user_model().objects.create_user(email, 'test123')

        self.assertEqual(user.email, email.lower())

    def test_new_user_invalid_email(self):
        """Test creating user with no email raises error"""
        # below test only passes if the function returns valueerror
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, 'test123')

    def test_create_supoer_user(self):
        """Test creating super user"""
        user = get_user_model().objects.create_superuser(
            'test@experiment.com',
            'experiment'
        )

        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)

    def test_tag_str(self):
        """Test the tag string representation"""
        tag = models.Tag.objects.create(
            user=sample_user(),
            name='Scripture'
        )

        self.assertEqual(str(tag), tag.name)

    def test_post_str(self):
        """Test the Post string representation"""
        post = models.Post.objects.create(
            author=sample_user(),
            title=''
        )

        self.assertEqual(str(post), post.title)
