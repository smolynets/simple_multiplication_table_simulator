from django.db import models


class FinishPerDay(models.Model):
    finish_time = models.CharField(max_length=50)
    score = models.CharField(max_length=10)
    spended_time = models.CharField(max_length=1000)
