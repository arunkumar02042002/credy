
from django.test import TestCase
from django.contrib.auth import get_user_model

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