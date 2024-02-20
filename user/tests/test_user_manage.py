from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.authtoken.models import Token

class AuthenticatedUserManageTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')
        self.client.force_authenticate(user=self.user)

    def test_user_list(self):
        url = reverse('user:list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_retrieve(self):
        url = reverse('user:profile')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.user.id)

    def test_user_update(self):
        url = reverse('user:profile')
        data = {
            'username': 'updatetestuser',
            'password': 'testpassword'
        }
        res = self.client.patch(url, data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['id'], self.user.id)
    
    def test_other_user_retrieve(self):
        # other user token adding
        other_user = get_user_model().objects.create(username='otheruser', password='otherpassword')
        token = Token.objects.create(user=other_user)

        url = reverse('user:profile')
        res = self.client.get(url, headers={'HTTP_AUTHORIZATION': 'Token ' + token.key})
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_other_user_update(self):
        # other user token adding
        other_user = get_user_model().objects.create(username='otheruser', password='otherpassword')
        token = Token.objects.create(user=other_user)

        url = reverse('user:profile')
        data = {
            'username': 'updatetestuser',
            'password': 'testpassword'
        }
        res = self.client.patch(url, data, HTTP_AUTHORIZATION='Token ' + token.key)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class UnAuthenticatedUserManageTest(APITestCase):

    def setUp(self):
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')

    def test_user_list(self):
        url = reverse('user:list')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_retrieve(self):
        url = reverse('user:profile')
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_update(self):
        url = reverse('user:profile')
        data = {
            'username': 'updatetestuser',
            'password': 'testpassword'
        }
        res = self.client.post(url, data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)