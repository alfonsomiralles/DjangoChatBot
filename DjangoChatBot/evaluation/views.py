from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from .models import Evaluation
from chatbot_app.models import PredefinedAnswer
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse
from datetime import datetime
from collections import defaultdict

@user_passes_test(lambda user: user.is_staff, login_url='login')
def evaluation_results(request):
    evaluations_list = Evaluation.objects.all().order_by('-timestamp')
    paginator = Paginator(evaluations_list, 10)
    page = request.GET.get('page')
    evaluations = paginator.get_page(page)

    context = {
        'evaluations': evaluations,
    }
    return render(request, 'evaluation/evaluation_results.html', context)

def chart_results(request):
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    else:
        start_date = None
    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = None
    evaluations_list = Evaluation.objects.all().order_by('-timestamp')

    # Aplicar filtros de fecha de inicio y fecha de finalización por separado
    if start_date:
        evaluations_list = evaluations_list.filter(timestamp__gte=start_date)
    if end_date:
        evaluations_list = evaluations_list.filter(timestamp__lte=end_date)

    paginator = Paginator(evaluations_list, 10)
    page = request.GET.get('page')
    evaluations = paginator.get_page(page)

    chart_data = generate_chart_data(start_date=start_date, end_date=end_date)

    context = {
        'evaluations': evaluations,
        'chart_data': json.dumps(chart_data),
        'start_date': start_date_str,
        'end_date': end_date_str,
    }
    return render(request, 'evaluation/chart_results.html', context)


@csrf_exempt
def update_user_rating(request):
    if request.method == "POST":
        data = json.loads(request.body)
        evaluation_id = data.get('evaluation_id')
        user_rating_choice = data.get('user_rating_choice')

        evaluation = Evaluation.objects.get(id=evaluation_id)
        evaluation.user_rating_choice = user_rating_choice
        evaluation.save()

        return JsonResponse({"status": "success"})
    else:
        return JsonResponse({"status": "failed"})

def generate_chart_data(start_date, end_date):
    evaluations = Evaluation.objects.all().order_by('timestamp')

    if start_date:
        evaluations = evaluations.filter(timestamp__gte=start_date)
    if end_date:
        evaluations = evaluations.filter(timestamp__lte=end_date)

    chart_data = defaultdict(lambda: {"U": 0, "N": 0, "NE": 0})
    for evaluation in evaluations:
        date = evaluation.timestamp.date()
        user_rating_choice = evaluation.user_rating_choice if evaluation.user_rating_choice else "NE"
        chart_data[date][user_rating_choice] += 1

    labels = []
    useful_ratings = []
    not_useful_ratings = []
    not_evaluated_ratings = []

    for date, counts in chart_data.items():
        labels.append(date.strftime('%Y-%m-%d'))
        useful_ratings.append(counts["U"])
        not_useful_ratings.append(counts["N"])
        not_evaluated_ratings.append(counts["NE"])

    context = {
        'labels': labels,
        'useful_ratings': useful_ratings,
        'not_useful_ratings': not_useful_ratings,
        'not_evaluated_ratings': not_evaluated_ratings,
    }
    return context