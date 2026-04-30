from django.db import models

from django.contrib.auth.models import User
from words.models import Lexeme
# Quiz -> Id, Questions, options, correct option


class Quiz(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Question(models.Model):
    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE, blank=True)
    text = models.CharField(max_length=255)

class Option(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="options")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
