from django.urls import path
from .views import chatbot
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('chatbot/', views.chatbot, name='chatbot'),
    path('manage_responses/', views.manage_responses, name='manage_responses'),
    path('edit_response/<int:response_id>/', views.edit_response, name='edit_response'),
    path('delete_response/<int:response_id>/', views.delete_response, name='delete_response'),
]