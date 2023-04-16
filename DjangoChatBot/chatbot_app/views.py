from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PredefinedAnswer
from .serializers import PredefinedAnswerSerializer
from .chatbot.chatbot import chatbot_get_answer

def index(request):
    return render(request, 'chatbot_app/index.html')

@api_view(['GET', 'POST'])
def chatbot(request):
    if request.method == 'POST':
        question = request.data.get('question', '')
        answer = chatbot_get_answer(question)
        return JsonResponse({"answer": answer})
    elif request.method == 'GET':
        answers = PredefinedAnswer.objects.all()
        serializer = PredefinedAnswerSerializer(answers, many=True)
        return Response(serializer.data)