from rest_framework import fields, serializers
from .models import Word, UserWord, Paragraph

class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        fields = ['id', 'text', 'definition', 'example']

class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWord
        fields = ['status']

class ParagraphSerializer(serializers.ModelSerializer):
    word_list = serializers.SerializerMethodField()

    def get_word_list(self, obj):
        return obj.text.split()
    
    class Meta:
        model = Paragraph
        fields = ['title', 'text', 'word_list']
