"""Testing the Question model."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """Create a question with the given `question_text`.

    Published the given number of `days` offset to now.
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionDetailViewTests(TestCase):
    """Tests for Question Detail View."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future.

        Return: a 404 if not found.
        """
        future_question = create_question(question_text='Future question.',
                                          days=5)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """Testing creates past questions to show detailed question text."""
        past_question = create_question(question_text='Past Question.', days=-5)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        index_response = self.client.get(response.url)
        self.assertContains(index_response, past_question.question_text, status_code=200)


class QuestionIndexViewTests(TestCase):
    """Tests for Question Index View."""

    def test_no_questions(self):
        """If no questions exist, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Past Questions are displayed on the index page."""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Future Questions aren't displayed on the index page."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Show Only past questions are displayed."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


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
