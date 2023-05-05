from django.db import models
from django.contrib.auth.models import User
from chatbot_app.models import PredefinedAnswer

class Evaluation(models.Model):
    USER_RATING_CHOICES = [
        ('U', 'Útil'),
        ('N', 'No útil'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.ForeignKey(PredefinedAnswer, on_delete=models.SET_NULL, null=True, blank=True)
    gpt_answer = models.TextField(blank=True, null=True)
    user_rating_choice = models.CharField(max_length=1, choices=USER_RATING_CHOICES, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.question}"
