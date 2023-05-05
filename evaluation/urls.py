from django.urls import path
from . import views

urlpatterns = [
    path('results/', views.evaluation_results, name='evaluation_results'),
    path('chart/', views.chart_results, name='chart_results'),
    path('update_rating/', views.update_user_rating, name='update_user_rating'),
]