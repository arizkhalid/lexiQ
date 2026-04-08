from rest_framework import viewsets
from rest_framework.response import Response
from .models import Word, UserWord, Paragraph
from .serializers import WordSerializer, UserWordSerializer, ParagraphSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.decorators import action


user = User.objects.first()  # temporary
class WordViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    @action(detail=False, url_path='by-slug/(?P<slug>[^/.]+)')
    def by_slug(self, request, slug=None):
        queryset = self.get_queryset().filter(text=slug)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    queryset = Word.objects.all()
    serializer_class = WordSerializer
    lookup_field = 'text'

class UserWordViewSet(viewsets.ModelViewSet):
    def create(self, request):
        word = Word.objects.get(text=request.data['word'])
        obj, created = UserWord.objects.update_or_create(
            user=user,
            word=word,
            defaults={'status': request.data['status'], 'score': 10}
        )
        serializer = UserWordSerializer(obj)
        return Response(serializer.data)
    # permission_classes = [IsAuthenticated]
    queryset = UserWord.objects.all()
    serializer_class = UserWordSerializer

class ParagraphViewSet(viewsets.ModelViewSet):
    # permission_classes = [IsAuthenticated]
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer
