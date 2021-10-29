"""Testing the Question model."""
import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question


class QuestionModelTests(TestCase):
    """Test for Question Model."""

    def test_was_published_recently_with_future_question(self):
        """was_published() Return: False for questions is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """was_published() Return:False for questions is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """was_published() Return:True for questions is within the last day."""
        time = timezone.now() - datetime.timedelta(hours=23,
                                                   minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """is_published() Return:False for questions is in the future."""
        time = timezone.now() + datetime.timedelta(days=20)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.is_published(), False)

    def test_is_published_with_published_question(self):
        """is_published() Return:True if current time is after published."""
        time = timezone.now() - datetime.timedelta(days=1)
        published_question = Question(pub_date=time)
        self.assertIs(published_question.is_published(), True)

    def test_can_vote_with_future_questions(self):
        """can_vote() Return:False for questions is in the future."""
        time = timezone.now() + datetime.timedelta(days=20)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.can_vote(), False)

    def test_can_vote_with_question_is_in_the_voting_period(self):
        """can_vote() Return:True if the voting is current time in period."""
        pub_date = timezone.now()
        end_date = timezone.now() + datetime.timedelta(days=5)
        question_is_in_the_voting_period = Question(pub_date=pub_date,
                                                    end_date=end_date)
        self.assertIs(question_is_in_the_voting_period.can_vote(), True)

    def test_can_vote_with_old_question_which_over_end_date(self):
        """can_vote() Return:False if the voting is a time over end_date."""
        pub_date = timezone.now() - datetime.timedelta(days=5)
        end_date = timezone.now() - datetime.timedelta(days=3)
        old_question = Question(pub_date=pub_date, end_date=end_date)
        self.assertIs(old_question.can_vote(), False)
