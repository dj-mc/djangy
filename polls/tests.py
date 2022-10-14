import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Question


def create_question(asked_question, days_til_pub=None):
    """Create a question with a date_published offset"""
    days_til_pub = days_til_pub or 0
    time = timezone.now() + datetime.timedelta(days=days_til_pub)
    return Question.objects.create(asked_question=asked_question, date_published=time)


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


class TestQuestionIndexView(TestCase):
    def test_no_questions_exist(self):
        """Handle when no questions exist"""

        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["last_five_questions"], [])

    def test_display_past_question(self):
        """Display questions whose date_published value is in the past"""
        one_month_old_question = create_question(
            asked_question="This question is 30 days old?", days_til_pub=-30
        )

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["last_five_questions"], [one_month_old_question]
        )

    def test_display_future_question(self):
        """
        Do *not* display questions whose date_published
        value is in the future
        """
        create_question(
            asked_question="This question is from the future?", days_til_pub=30
        )

        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context["last_five_questions"], [])

    def test_display_future_and_past_question(self):
        """Display past questions while ignoring future questions"""
        create_question(
            asked_question="This question is from the future?", days_til_pub=30
        )
        one_month_old_question = create_question(
            asked_question="This question is 30 days old?", days_til_pub=-30
        )

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["last_five_questions"], [one_month_old_question]
        )

    def test_display_two_past_questions(self):
        """Display two questions whose date_published value is in the past"""
        past_question_1 = create_question(
            asked_question="Past question 1?", days_til_pub=-30
        )
        past_question_2 = create_question(
            asked_question="Past question 2?", days_til_pub=-15
        )

        response = self.client.get(reverse("polls:index"))
        self.assertQuerysetEqual(
            response.context["last_five_questions"], [past_question_2, past_question_1]
        )


class TestQuestionDetailsView(TestCase):
    def test_future_question_details(self):
        """Return status code 404 if the question is not yet published"""
        not_yet_published_question = create_question(
            asked_question="Publish me in 5 days?", days_til_pub=5
        )

        url = reverse("polls:details", args=(not_yet_published_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question_details(self):
        """Return the details page for any past question and their poll"""
        already_published_question = create_question(
            asked_question="Already published 2 days ago?", days_til_pub=-2
        )

        url = reverse("polls:details", args=(already_published_question.id,))
        response = self.client.get(url)
        self.assertContains(response, already_published_question.asked_question)
