from django.db import models
from django.contrib.auth.models import User


# TODO what to do with same words with different meanings
class Word(models.Model):
    REGISTER_CHOICES = [
        ("formal", "Formal"),
        ("informal", "Informal"),
        ("slang", "Slang"),
    ]

    CONNOTATION_CHOICES = [
        ("positive", "Positive"),
        ("negative", "Negative"),
        ("neutral", "Neutral"),
    ]

    text = models.CharField(max_length=100)
    definition = models.TextField()
    example = models.TextField()

    part_of_speech = models.CharField(max_length=50, blank=True, default="")
    synonyms = models.JSONField(default=list, blank=True)
    antonyms = models.JSONField(default=list, blank=True)
    usage = models.TextField(blank=True, default="")
    examples = models.JSONField(default=list, blank=True)
    register = models.CharField(
        max_length=20, choices=REGISTER_CHOICES, blank=True, default=""
    )
    connotation = models.CharField(
        max_length=20, choices=CONNOTATION_CHOICES, blank=True, default=""
    )
    collocations = models.JSONField(default=list, blank=True)
    word_forms = models.JSONField(default=dict, blank=True)

    def __str__(self) -> str:
        return self.text


STATUS = [("weak", "weak"), ("known", "known")]


class UserWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Word, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=10)
    # TODO add a score
    score = models.IntegerField()

    def __str__(self) -> str:
        return self.word.text


class Paragraph(models.Model):
    title = models.CharField(max_length=100, default="")
    text = models.TextField()
    def __str__(self) -> str:
        return self.title
