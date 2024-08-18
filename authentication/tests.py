
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()

class UserModelTest(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_user(
            email='test@gmail.com',
            username='test_user',
            first_name='Test',
            last_name='User',
            password='testpassword'
        )
        self.superuser = User.objects.create_superuser(
            email='admin@gmail.com',
            username='admin123',
            first_name='Admin',
            last_name='User',
            password='testpassword'
        )

    def test_create_user(self):
        self.assertEqual(self.user.email, 'test@gmail.com')
        self.assertEqual(self.user.username, 'test_user')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertTrue(self.user.check_password('testpassword'))
        self.assertFalse(self.user.is_staff)
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_superuser)

    def test_create_superuser(self):
        self.assertEqual(self.superuser.email, 'admin@gmail.com')
        self.assertEqual(self.superuser.username, 'admin123')
        self.assertEqual(self.superuser.first_name, 'Admin')
        self.assertEqual(self.superuser.last_name, 'User')
        self.assertTrue(self.superuser.check_password('testpassword'))
        self.assertTrue(self.superuser.is_staff)
        self.assertTrue(self.superuser.is_active)
        self.assertTrue(self.superuser.is_superuser)


class RegisterUserViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('register')
        self.valid_payload = {
            "username": "newuser",
            "password": "strongpassword123"
        }
        self.invalid_payload = {
            "username": "newuser",
            "password": "123" 
        }

    def test_register_user_success(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('access', response.data)
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_user_invalid_password(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)
        self.assertFalse(User.objects.filter(username="newuser").exists())

    def test_register_user_missing_fields(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)


class LoginUserViewTest(APITestCase):

    def setUp(self):
        self.url = reverse('login')
        self.username = "testuser"
        self.password = "strongpassword123"
        self.user = User.objects.create_user(username=self.username, password=self.password)
        self.valid_payload = {
            "username": self.username,
            "password": self.password
        }
        self.invalid_payload = {
            "username": self.username,
            "password": "wrongpassword"
        }

    def test_login_user_success(self):
        response = self.client.post(self.url, data=self.valid_payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_login_user_invalid_credentials(self):
        response = self.client.post(self.url, data=self.invalid_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('non_field_errors', response.data)

    def test_login_user_missing_fields(self):
        response = self.client.post(self.url, data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)
        self.assertIn('password', response.data)