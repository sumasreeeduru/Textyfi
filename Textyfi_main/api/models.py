from django.db import models



class wordcounterModel(models.Model):
    sentence = models.TextField()
    count=models.IntegerField()
class ratereviewModel(models.Model):
    review=models.TextField()
    rating=models.FloatField()
class grammarModel(models.Model):
    text=models.TextField()
    grammar=models.TextField()

    

    