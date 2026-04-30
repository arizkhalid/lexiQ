from django.db import models

from django.contrib.auth.models import User
from words.models import Lexeme
# Quiz -> Id, Questions, options, correct option


class Question(models.Model):
    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE, blank=True)
    text = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.id} {self.lexeme.word}"

class Quiz(models.Model):
    STATE_CHOICES = [
        ("not_started", "Not Started"),
        ("pending", "Pending"),
        ("ended", "Ended"),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    state = models.CharField(max_length=20)
    questions = models.ManyToManyField(Question)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
