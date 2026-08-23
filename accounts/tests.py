from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

class AccountAccessTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='testpassword')

    def test_login_page_loads(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_register_page_loads(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_profile_requires_login(self):
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  

    def test_inbox_requires_login(self):
        response = self.client.get(reverse('accounts:inbox'))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_access_profile(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_logged_in_user_can_access_inbox(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('accounts:inbox'))
        self.assertEqual(response.status_code, 200)        
