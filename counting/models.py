from django.db import models
from solo.models import SingletonModel


class FinishPerDay(models.Model):
    finish_time = models.CharField(max_length=50)
    score = models.CharField(max_length=10)
    spended_time = models.CharField(max_length=1000)


class SiteConfiguration(SingletonModel):
    greeting_text = models.TextField()

    def __str__(self):
        return "Site Configuration"

    class Meta:
        verbose_name = "Site Configuration"
