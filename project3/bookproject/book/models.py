from django.db import models

class SampleModel(models.Model):
    title = models.CharField(max_length=100)
    number = models.IntegerField()
