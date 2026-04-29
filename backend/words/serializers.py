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

    def get_word_list(self, obj):
        return obj.text.split()

    class Meta:
        model = Paragraph
        fields = ["title", "text", "word_list"]
