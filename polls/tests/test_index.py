"""Testing the Question Index View model."""
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
    end_time = timezone.now() + datetime.timedelta(days=end)
    return Question.objects.create(question_text=question_text, pub_date=pub_date, end_date=end_time)


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
        create_question(question_text="Past question.", start=-30, end=-15)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Future Questions aren't displayed on the index page."""
        create_question(question_text="Future question.", start=30, end=35)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Show Only past questions are displayed."""
        create_question(question_text="Past question.", start=-10, end=-5)
        create_question(question_text="Future question.", start=4, end=10)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", start=-30,end=-25)
        create_question(question_text="Past question 2.", start=-5, end=-2)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )
