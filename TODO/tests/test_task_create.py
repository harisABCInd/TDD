import datetime
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model
from core.models import Task, Tag
from faker import Faker
from django.urls import reverse
import random

class BaseTaskCreateTestCase(APITestCase):

    def setUp(self):
        self.fake = Faker()
        self.users = self.create_test_users()
        self.tags = self.create_test_tags()
        self.user = random.choice(self.users)
        self.other_user = random.choice(self.users)

    def create_test_users(self):
        # Create users
        users = []
        for _ in range(5):  # Change the number of users as needed
            user = get_user_model().objects.create_user(
                username=self.fake.user_name(),
                password='password'  # You can use any password for dummy data
            )
            users.append(user)
        return users
    
    def create_test_tags(self):
        # Create tags
        tags = []
        for _ in range(5):  # Change the number of tags as needed
            tag = Tag.objects.create(name=self.fake.word())
            tags.append(tag)
        return tags


class AuthenticatedUserTaskCreateTestCase(BaseTaskCreateTestCase):
    def setUp(self):
        super().setUp()
        self.client.force_authenticate(user=self.user)
        self.data = {
            "name": self.fake.sentence(),
            "is_complete": random.choice([True, False]),
            "created_by": self.user,
            "priority": random.choice(['low', 'medium', 'high']),
            "due_date": self.fake.future_date(),
            "notes": self.fake.text(),
            "completion_date": self.fake.future_date(),
            "assigned_to": self.other_user,
        }

    def test_create_task_success(self):
        url = reverse('TODO:tasks-list')
        res = self.client.post(url, self.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_task_with_passed_due_date(self):
        url = reverse('TODO:tasks-list')
        self.data['due_date'] = datetime.datetime.now(-10)
        res = self.client.post(url, self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_no_created_by_user(self):
        url = reverse('TODO:tasks-list')
        self.data['created_by'] = None
        res = self.client.post(url, self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_task_with_no_assigned_to_user(self):
        url = reverse('TODO:tasks-list')
        self.data['assigned_to'] = None
        res = self.client.post(url, self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_task_name_is_required(self):
        url = reverse('TODO:tasks-list')
        self.data['name'] = ""
        res = self.client.post(url, self.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

class UnAuthenticatedUserTaskCreateTestCase(BaseTaskCreateTestCase):
    def setUp(self):
        super().setUp()
        self.data = {
            "name": self.fake.sentence(),
            "is_complete": random.choice([True, False]),
            "created_by": self.user,
            "priority": random.choice(['low', 'medium', 'high']),
            "due_date": self.fake.future_date(),
            "notes": self.fake.text(),
            "completion_date": self.fake.future_date(),
            "assigned_to": self.other_user,
        }
    
    def test_create_task_failure(self):
        url = reverse('TODO:tasks-list')
        res = self.client.post(url, self.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)