from django.db import models

# Create your models here.


class PredefinedAnswer(models.Model):
    answer = models.TextField()
    keywords = models.TextField()

    def __str__(self):
        return self.answer