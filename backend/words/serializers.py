from rest_framework import fields, serializers
from .models import Word, UserWord, Paragraph


class WordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Word
        # include the examples JSONField and avoid duplicate 'example' entry
        fields = [
            "id",
            "text",
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
