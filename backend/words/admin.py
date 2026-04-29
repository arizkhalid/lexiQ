from django.contrib import admin
from .models import WordSense, UserWord, Paragraph, Lexeme

admin.site.register(WordSense)
admin.site.register(UserWord)
admin.site.register(Paragraph)
admin.site.register(Lexeme)
