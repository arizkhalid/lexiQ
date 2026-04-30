from rest_framework import serializers
from .models import Question, Option
class GenerateQuizSerializer(serializers.Serializer):
    id = serializers.IntegerField()

class QuestionSerializer(serializers.ModelSerializer):
    options = serializers.SerializerMethodField()
    def get_options(self, obj):
        res = list(Option.objects.filter(question=obj))
        return [o.text for o in res]

    class Meta:
        model = Question
        fields = [
            "id",
            "text",
            "options"
        ]
