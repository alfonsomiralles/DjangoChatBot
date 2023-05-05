from rest_framework import serializers
from .models import PredefinedAnswer

class PredefinedAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = PredefinedAnswer
        fields = ['id', 'answer', 'keywords']