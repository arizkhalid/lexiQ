from rest_framework.views import APIView, Response, status
from words.models import UserWord
from .models import Option, Quiz, Question
from .serializers import GenerateQuizSerializer, QuestionSerializer
from rest_framework.permissions import IsAuthenticated
import random

class GenerateQuizView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        user = request.user
        words = UserWord.objects.filter(user=user).select_related('word')
        data = [ w.word.word for w in words]
        random.shuffle(data)

        print("Words", data)
        quiz = Quiz.objects.create(user=user)
        question_list = []
        for word in data:
            q = list(Question.objects.filter(lexeme=word))
            if q:
                random.shuffle(q)
                question_list.extend(q[:random.randint(1, 2)])
                if len(question_list) >= 10:
                    break
            else:
                continue
        if len(question_list) < 10:
            random_questons = list(Question.objects.all().order_by('?')[:10-len(question_list)])
            question_list.extend(random_questons)
        print(question_list)
        quiz.questions.set(question_list) 
        quiz.save()
        random_q = quiz.questions.all().order_by('?').first()
        res = QuestionSerializer(random_q)
        return Response({'quiz_id': quiz.id, 'question': res.data}, status=status.HTTP_201_CREATED)

class McqSolvedView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        quiz_id = int(request.data.get('quiz_id'))
        mcq_id = int(request.data.get('mcq_id'))
        selected = request.data.get('selected')

        quiz = Quiz.objects.get(id=quiz_id)
        question = Question.objects.get(id=mcq_id)
        option = Option.objects.get(question=question, text=selected) 
        correct_option = Option.objects.get(question=question, is_correct=True);
         
        quiz.questions.remove(question)
        random_q = quiz.questions.all().order_by('?').first()
        if not random_q:
            return Response({'ended': True, 'correct': option.is_correct, 'correct_option': correct_option.text})
        res = QuestionSerializer(random_q)
        

        return Response({'correct': option.is_correct, 'next': res.data, 'correct_option': correct_option.text})
