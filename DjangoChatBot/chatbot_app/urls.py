from django.urls import path
from .views import chatbot
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('manage_responses/', views.manage_responses, name='manage_responses'),
]