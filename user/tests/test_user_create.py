from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth import get_user_model

# Create your tests here.

class CreateUserTests(APITestCase):
    def test_create_user_success(self):
        url = reverse('user:create')

        data = {
            "username": "TestUser",
            "email": "TestUser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestUser123",
            "confirm_password": "TestUser123",
        }

        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertNotIn("password", res.data)

    def test_create_user_with_short_password (self):
        url = reverse('user:create')
        data = {
            "username": "TestUser",
            "email": "TestUser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "test",
            "confirm_password": "test",
        }

        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(username=data['username']).exists()
        self.assertFalse(user_exists)
    
    def test_create_user_with_username_already_exists(self):
        user = get_user_model().objects.create(username="TestUser")

        url = reverse('user:create')
        data = {
            "username": "TestUser",
            "email": "TestUser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestUser123",
            "confirm_password": "TestUser123",
        }

        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_user_password_doesnot_match(self):
        url = reverse('user:create')

        data = {
            "username": "TestUser",
            "email": "TestUser@example.com",
            "first_name": "Test",
            "last_name": "User",
            "password": "TestUser123",
            "confirm_password": "TestUser1234",
        }

        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

