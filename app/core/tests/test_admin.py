from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


# we can get User anywhere after we setup User
# in the Django settings
class AdminSiteTests(TestCase):

    def setUp(self):
        """Initial configuration for all the tests"""
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email='admin@experiment.com',
            password='experiment'
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email='test@experiment.com',
            password='experiment',
            first_name='Test User Full Name'
        )
# we don't have username so we make few changes for admin #C1, C2

    def test_users_listed(self):
        """Test that users are listed on user page"""
        # before colon "APP" then "URL",
        # core_user_changelist are defined in django admin documentation
        # we also have to create url for core_user_changelist
        url = reverse('admin:core_user_changelist')
        res = self.client.get(url)

        self.assertContains(res, self.user.first_name)
        self.assertContains(res, self.user.email)

    def test_user_change_page(self):
        """Test that the user edit page works"""
        url = reverse('admin:core_user_change', args=[self.user.id])
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)

    def test_create_user_page(self):
        """Test that the create user page works"""
        url = reverse('admin:core_user_add')
        res = self.client.get(url)

        self.assertEqual(res.status_code, 200)
