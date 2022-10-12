import datetime
from django.test import TestCase
from django.utils import timezone
from .models import Question


class TestQuestionModel(TestCase):  # django.test.TestCase subclass
    def test_was_recently_published_on_old_question(self):
        """
        was_recently_published() returns False on questions
        whose date_published value is older than one day
        """
        over_24_hours_ago = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(date_published=over_24_hours_ago)
        self.assertIs(old_question.was_recently_published(), False)

    def test_was_recently_published_on_recent_question(self):
        """
        was_recently_published() returns True on questions
        whose date_published value is within the last day
        """
        within_last_24_hours = timezone.now() - datetime.timedelta(
            hours=23, minutes=59, seconds=59
        )
        recent_question = Question(date_published=within_last_24_hours)
        self.assertIs(recent_question.was_recently_published(), True)

    def test_was_recently_published_on_future_question(self):
        """
        was_recently_published() returns False on questions
        whose date_published value is in the future
        """
        one_month_from_now = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(date_published=one_month_from_now)
        self.assertIs(future_question.was_recently_published(), False)
