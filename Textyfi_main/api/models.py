from django.db import models

# Create your models here.
# class reviewratingModel(models.Model):
#     review=models.TextField()
#     rating = models.IntegerField()

class wordcounterModel(models.Model):
    sentence = models.TextField()
    count=models.IntegerField()

    