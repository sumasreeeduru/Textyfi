from rest_framework import serializers
from .models import wordcounterModel
# class reviewratingSerializer(serializers.Serializers):
#     review=serializers.CharField()
#     rating=serializers.IntegerField()
#     def create(self,validated_data):
#         return reviewratingModel(**validated_data)
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