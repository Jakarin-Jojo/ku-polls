"""Tests of authentication."""
import django.test
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from polls.models import Question, Choice


class UserAuthTest(django.test.TestCase):

    def setUp(self):
        """Set up a user and question for the test."""
        super().setUp()
        self.username = "testuser"
        self.password = "Fat-Chance!"
        self.user1 = User.objects.create_user(
            username=self.username,
            password=self.password,
            email="testuser@nowhere.com")
        self.user1.first_name = "Tester"
        self.user1.save()
        # need a poll question to test voting
        pub_date = timezone.now()
        end_date = timezone.now() + datetime.timedelta(days=5)
        q = Question.objects.create(question_text="First Poll Question", pub_date=pub_date, end_date=end_date)
        q.save()
        # a few choices
        for n in range(1, 4):
            choice = Choice(choice_text=f"Choice {n}", question=q)
            choice.save()
        self.question = q

    def test_login_view(self):
        """Test that a user can login via the login view."""
        login_url = reverse("login")
        # Can get the login page
        response = self.client.get(login_url)
        self.assertEqual(200, response.status_code)
        # Can login using POST
        # usage: client.post(url, {'key1":"value", "key2":"value"})
        form_data = {"username": "testuser",
                     "password": "Fat-Chance!"
                     }
        response = self.client.post(login_url, form_data)
        self.assertEqual(302, response.status_code)
        # should redirect us to the polls index page ("polls:index")
        self.assertRedirects(response, reverse("polls:index"))