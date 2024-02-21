from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

class UserLoginTests(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(username="TestUser", password="TestPassword")

    def test_user_login_success(self):
        """User get status 200 and check if data has token """
        url = reverse('user:login')
        data = {
            'username': "TestUser",
            'password': "TestPassword"
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn('token', res.data)
    
    def test_user_login_failure(self):
        """
        Invalid username and password
        """
        url = reverse('user:login')
        data = {
            'username': "TestUser123",
            'password': "TestPassword"
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_inactive_login_failure(self):
        """
        User is not active failure
        """
        url = reverse('user:login')
        self.user.is_active = False
        self.user.save()
        data = {
            'username': "TestUser",
            'password': "TestPassword"
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
