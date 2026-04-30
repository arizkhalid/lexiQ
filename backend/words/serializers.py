from rest_framework import fields, serializers
from .models import WordSense, Lexeme, UserWord, Paragraph

class LexemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lexeme
        fields = ["word"]

class WordSenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = WordSense
        fields = [
            "id",
            "lexeme",
            "definition",
            "example",
            "part_of_speech",
            "synonyms",
            "antonyms",
            "usage",
            "examples",
            "register",
            "connotation",
            "collocations",
            "word_forms",
        ]


class UserWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserWord
        fields = ["status"]


class ParagraphSerializer(serializers.ModelSerializer):
    word_list = serializers.SerializerMethodField()
    word_length = serializers.SerializerMethodField()

    def get_word_list(self, obj):
        res = []
        text = obj.text
        start = 0
        for i in range(len(text)):
            if not text[i].isalpha():
                res.append(text[start:i])
                res.append(text[i])
                start = i+1
        return res

    def get_word_length(self, obj):
        return len(obj.text.split())

    class Meta:
        model = Paragraph
        fields = ["id", "title", "text", "word_list", "difficulty", "source", "word_length"]
