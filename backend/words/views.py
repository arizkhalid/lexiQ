from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import WordSense, Lexeme, UserWord, Paragraph
from .serializers import WordSenseSerializer, UserWordSerializer, ParagraphSerializer, LexemeSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

class WordAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, word):
        lexeme = get_object_or_404(Lexeme, word=word.lower())
        senses = WordSense.objects.filter(lexeme=lexeme)
        data = WordSenseSerializer(senses, many=True).data
        return Response(data) 
        

class UserWordViewSet(viewsets.ModelViewSet):
    def create(self, request):
        user = request.user
        word = Lexeme.objects.get(word=request.data['word'])
        obj, created = UserWord.objects.update_or_create(
            user=user,
            word=word,
            defaults={'status': request.data['status']}
        )
        serializer = UserWordSerializer(obj)
        return Response(serializer.data)
    permission_classes = [IsAuthenticated]
    queryset = UserWord.objects.all()
    serializer_class = UserWordSerializer

class ParagraphViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Paragraph.objects.all()
    serializer_class = ParagraphSerializer
