from django.db import models
from django.contrib.auth.models import User


# TODO what to do with same words with different meanings
class Lexeme(models.Model):
    word = models.CharField(max_length=100, primary_key=True)

class WordSense(models.Model):
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
    lexeme = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
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
        return self.lexeme.word


STATUS = [("weak", "weak"), ("known", "known")]


class UserWord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    word = models.ForeignKey(Lexeme, on_delete=models.CASCADE)
    status = models.CharField(choices=STATUS, max_length=10)

    def __str__(self) -> str:
        return self.word.text


class Paragraph(models.Model):
    DIFFICULTY_CHOICES = [
        ("Easy", "Easy"),
        ("Medium", "Medium"),
        ("Hard", "Hard")
    ]
    title = models.CharField(max_length=100, default="")
    text = models.TextField()
    difficulty = models.CharField(
        max_length=20, choices=DIFFICULTY_CHOICES
    )
    source = models.CharField(max_length=100, blank=True)
    def __str__(self) -> str:
        return self.title
