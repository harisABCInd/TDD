from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status

class BaseUserTestCase(APITestCase):
    """
    Base test case class for user-related tests.

    Provides common setup and assertion methods for user tests.
    """

    def setUp(self):
        """
        Set up a test user.
        """
        self.user = get_user_model().objects.create(username='testuser', password='testpassword')

    def assert_authenticated_response(self, response, status_code=status.HTTP_200_OK):
        """
        Asserts that the response is successful and contains user information.

        Args:
            response: The HTTP response object.
            status_code: Expected HTTP status code.

        Raises:
            AssertionError: If assertion fails.
        """
        self.assertEqual(response.status_code, status_code)
        

    def assert_unauthenticated_response(self, response, status_code=status.HTTP_401_UNAUTHORIZED):
        """
        Asserts that the response indicates unauthenticated access.

        Args:
            response: The HTTP response object.
            status_code: Expected HTTP status code.

        Raises:
            AssertionError: If assertion fails.
        """
        self.assertEqual(response.status_code, status_code)

class AuthenticatedUserManageTest(BaseUserTestCase):
    """
    Test case class for user management by an authenticated user.
    """

    def setUp(self):
        """
        Set up an authenticated test user.
        """
        super().setUp()
        self.client.force_authenticate(user=self.user)

    def test_user_list(self):
        """
        Test retrieving the list of users by an authenticated user.
        """
        url = reverse('user:list')
        res = self.client.get(url)
        self.assert_authenticated_response(res)

    def test_user_retrieve(self):
        """
        Test retrieving the user profile by an authenticated user.
        """
        url = reverse('user:profile')
        res = self.client.get(url)
        self.assert_authenticated_response(res)
    
    def test_user_update(self):
        """
        Test updating the user profile by an authenticated user.
        """
        url = reverse('user:profile')
        data = {
            'username': 'updatetestuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        }
        res = self.client.patch(url, data)
        self.assert_authenticated_response(res)
        self.assertEqual(res.data['id'], self.user.id)
        user_exists = get_user_model().objects.filter(username=res.data['username']).exists()
        self.assertTrue(user_exists)

    def test_user_update_with_password_not_match(self):
        """
        Test updating the user profile by an authenticated user.
        """
        url = reverse('user:profile')
        data = {
            'username': 'updatetestuser',
            'password': 'testpassword',
            'confirm_password': 'testpassword123'
        }
        res = self.client.patch(url, data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
class UnAuthenticatedUserManageTest(BaseUserTestCase):
    """
    Test case class for user management by an unauthenticated user.
    """

    def test_user_list(self):
        """
        Test accessing the list of users by an unauthenticated user.
        """
        url = reverse('user:list')
        res = self.client.get(url)
        self.assert_unauthenticated_response(res)

    def test_user_retrieve(self):
        """
        Test accessing the user profile by an unauthenticated user.
        """
        url = reverse('user:profile')
        res = self.client.get(url)
        self.assert_unauthenticated_response(res)

    def test_user_update(self):
        """
        Test updating the user profile by an unauthenticated user (should be forbidden).
        """
        url = reverse('user:profile')
        data = {'username': 'updatetestuser', 'password': 'testpassword'}
        res = self.client.patch(url, data)
        self.assert_unauthenticated_response(res)
