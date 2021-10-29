"""Testing the Question model."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from polls.models import Question


def create_question(question_text, start, end):
    """Create a question with the given `question_text`.

    Published the given number of `days` offset to now.
    """
    pub_date = timezone.now() + datetime.timedelta(days=start)
    end_date = timezone.now() + datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text, pub_date=pub_date, end_date=end_date)


class QuestionDetailViewTests(TestCase):
    """Tests for Question Detail View."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future.

        Return: a 404 if not found.
        """
        future_question = create_question(question_text='Future question.',
                                          start=5, end=10)
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """Testing creates past questions to show detailed question text."""
        past_question = create_question(question_text='Past Question.', start=-5, end=-1)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        index_response = self.client.get(response.url)
        self.assertContains(index_response, past_question.question_text, status_code=200)
