from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from datetime import date   
from opportunities.models import Opportunity
from accounts.models import Application, Message

from accounts.models import Application

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


class AccountFormTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

        self.opportunity = Opportunity.objects.create(
            title='Test Opportunity', organization="Test Organization", location="Dublin", date=date.today(), spaces_available=5, description="Test Volunteer Opportunity", is_active=True, category="community")
    def test_user_can_apply_for_opportunity(self):
            self.client.login(username='testuser', password='testpassword')
            response = self.client.post(reverse('accounts:apply', args=[self.opportunity.id]))
            self.assertEqual(response.status_code, 302)  
            self.assertTrue(Application.objects.filter(user=self.user, opportunity=self.opportunity).exists())

    def test_duplicate_application_is_not_created(self):
            self.client.login(username='testuser', password='testpassword')
            self.client.post(reverse('accounts:apply', args=[self.opportunity.id]))
            response = self.client.post(reverse('accounts:apply', args=[self.opportunity.id]))
            self.assertEqual(response.status_code, 302)  
            applications = Application.objects.filter(user=self.user, opportunity=self.opportunity)
            self.assertEqual(applications.count(), 1)

    def test_my_applications_only_show_current_user_applications(self):
            self.client.login(username='testuser', password='testpassword')
            Application.objects.create(user=self.user, opportunity=self.opportunity)
            Application.objects.create(user=self.other_user, opportunity=self.opportunity)
            response = self.client.get(reverse('accounts:my_applications'))
            self.assertEqual(response.status_code, 200)
            applications = response.context['applications']
            self.assertEqual(len(applications), 1)  
            self.assertEqual(applications[0].user, self.user)       


class MessagingTests(TestCase):
     def setUp(self):
          self.sender = User.objects.create_user(username="sender", password="testpassword",)
          self.recipient = User.objects.create_user(username="recipient", password="testpassword",)
          self.other_user = User.objects.create_user(username="other", password="testpassword",)
     def test_user_can_send_message(self):
         self.client.login(username="sender", password="testpassword",)
         response = self.client.post(reverse("accounts:send_message"),{"recipient":self.recipient.id, "subject": "Test message", "body": "Hello from the automated test",},)

         self.assertEqual(response.status_code, 302)

         message = Message.objects.get(
            subject="Test message"
        )

         self.assertEqual(message.sender, self.sender)
         self.assertEqual(message.recipient, self.recipient)

     def test_recipient_can_archive_message(self):
        message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject="Archive me",
            body="Test message",
        )

        self.client.login(
            username="recipient",
            password="testpassword",
        )

        response = self.client.post(
            reverse(
                "accounts:archive_message",
                args=[message.id],
            )
        )

        self.assertEqual(response.status_code, 302)

        message.refresh_from_db()

        self.assertTrue(message.archived)

     def test_other_user_cannot_archive_someone_elses_message(self):
        message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            subject="Private message",
            body="This belongs to the recipient.",
        )

        self.client.login(
            username="other",
            password="testpassword",
        )

        response = self.client.post(
            reverse(
                "accounts:archive_message",
                args=[message.id],
            )
        )

        self.assertEqual(response.status_code, 404)

        message.refresh_from_db()
              