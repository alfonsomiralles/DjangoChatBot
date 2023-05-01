from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.decorators import user_passes_test
from .models import Evaluation
from django.views.decorators.csrf import csrf_exempt
import json
from django.http import JsonResponse

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
