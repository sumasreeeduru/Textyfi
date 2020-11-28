from rest_framework import serializers
from .models import wordcounterModel
from texthandwritten.models import texthand
from django.http import JsonResponse,HttpResponse
class wordcounteSerializer(serializers.Serializer):
    sentence=serializers.CharField()
    count = serializers.IntegerField()
    def create(self,validated_data):
        return wordcounterModel(**validated_data)
    def update(self,instance,validated_data):
        instance.sentence=validated_data.get('sentence',instance.sentence)
        instance.count=validated_data.get('count',instance.count)
        instance.save()
        return instance
class texthandSerializer(serializers.Serializer):
    sentence = serializers.CharField()
    pdffile=serializers.FileField()
    def create(self,validated_data):
        return texthand(**validated_data)
    def update(self,instance,validated_data):
        instance.sentence = validated_data.get('sentence',instance.sentence)
        instance.pdffile =  validated_data.get('pdffile',"media/outputs/output.pdf")
        instance.save()
        return instance