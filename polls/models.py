from django.db import models
from django.utils import timezone
from datetime import datetime


class Question(models.Model):
    def __str__(self) -> str:
        return self.asked_question

    asked_question = models.CharField(max_length=200)
    date_published = models.DateTimeField("date published")

    def was_recently_published(self) -> bool:
        return self.date_published >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
    def __str__(self) -> str:
        return self.question_choice

    # Each choice is related to a single question
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    question_choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
