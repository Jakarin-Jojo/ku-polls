import datetime
from django.db import models
from django.utils import timezone
from django.contrib import admin


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('end date')

    def __str__(self):
        return self.question_text

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='Published recently ?'
    )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='IS PUBLISHED'
    )
    def is_published(self):
        """Return: True if the current time is on or after questions publication time"""
        return timezone.now() >= self.pub_date

    @admin.display(
        boolean=True,
        ordering='pub_date',
        description='CAN VOTE'
    )
    def can_vote(self):
        """Return: True if the voting is currently in equal or after pub_date and not over end_date."""
        return self.pub_date <= timezone.now() <= self.end_date


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
