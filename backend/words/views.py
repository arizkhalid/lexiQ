from rest_framework import viewsets
from .models import Word, UserWord, Paragraph
from .serializers import WordSerializer, UserWordSerializer, ParagraphSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny

class WordViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = 'text'

class UserWordViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = UserWord.objects.all()
    serializer_class = UserWordSerializer

class ParagraphViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer
