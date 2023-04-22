from django.shortcuts import render, redirect
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import PredefinedAnswer
from .serializers import PredefinedAnswerSerializer
from .chatbot.chatbot import chatbot_get_answer
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import PredefinedAnswerForm

@login_required
def index(request):
    return render(request, 'index.html')

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
    
@user_passes_test(lambda user: user.is_staff, login_url='login')
def manage_responses(request):
    if request.method == 'POST':
        form = PredefinedAnswerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_responses')
    query = request.GET.get('search')
    if query:
        responses = PredefinedAnswer.objects.filter(keywords__icontains=query)
    else:
        responses = PredefinedAnswer.objects.all()
    form = PredefinedAnswerForm()

    context = {
        'responses': responses,
        'form': form
    }
    return render(request, 'chatbot_app/manage_responses.html', context)    