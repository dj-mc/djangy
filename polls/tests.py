import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question


class TestQuestionModel(TestCase):  # django.test.TestCase subclass
    def test_was_recently_published_on_future_question(self):
        """
        was_recently_published() returns False on questions
        whose date_published value is in the future
        """
        one_month_from_now = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(date_published=one_month_from_now)
        self.assertIs(future_question.was_recently_published(), False)
