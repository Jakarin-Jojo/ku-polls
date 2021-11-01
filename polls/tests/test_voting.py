"""Tests of authentication Vote."""
import django.test
import datetime
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from polls.models import Question, Choice


class VoteModelTests(django.test.TestCase):

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

    def test_auth_required_to_vote(self):
        """Test that authentication is required to submit a vote.

        As an unauthenticated user,
        When I submit a vote for a question,
        Then I receive a 403 status code response
          Or I am redirected to the login page
        """
        vote_url = reverse('polls:vote', args=[self.question.id])

        # what choice to vote for?
        choice = self.question.choice_set.first()
        # the polls detail page has a form, each choice is identified by its id
        form_data = {"choice": f"{choice.id}"}
        response = self.client.post(vote_url, form_data)
        self.assertEqual(response.status_code, 302)
