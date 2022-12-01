import datetime

from django.db import models
from django.contrib import admin
from django.utils import timezone


class Question(models.Model):
    def __str__(self) -> str:
        return self.asked_question

    asked_question = models.CharField(max_length=200)
    date_published = models.DateTimeField("date published")

    @admin.display(
        boolean=True,  # Green checkmark
        ordering=date_published,  # Order by another field
        # Replace variable name with description
        description="Published recently?",
    )
    def was_recently_published(self) -> bool:
        now = timezone.now()  # Is date_published between 24 hours and now?
        return now - datetime.timedelta(days=1) <= self.date_published <= now


class Choice(models.Model):
    def __str__(self) -> str:
        return self.question_choice

    # ForeignKey fields display a <select> box, and also
    # provide a "(+) Add another..." button on admin page
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    # Each choice is related to a single question
    question_choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
