from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
# Create your views here.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob 
import re
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .serializers import wordcounteSerializer
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import wordcounterModel

#from app.views import temp_view 
@api_view(['GET'])
def api_index_view(request):
    return HttpResponse("Works")

@api_view(['GET'])
def ratereview(request,review):

    a1 = SentimentIntensityAnalyzer()
    vs=a1.polarity_scores(review)

    if vs['neu']==1:
        a2=TextBlob(review)
        if a2.sentiment.polarity==0:
            rating=1
            return HttpResponse(str(rating))
    if vs['compound'] < 0 and vs['neg']>0.3 and vs['pos']==0:
        rating = 1
        return HttpResponse(str(rating))
    if vs['compound'] > 0 and vs['pos']>0.3 and vs['neg']==0:
        rating = 5
        return HttpResponse(str(rating))
    if vs['neg']>vs['pos'] and vs['neg']>0.5 and vs['pos']!=0 :
        rating = 2
        return HttpResponse(str(rating))
    if vs['neg']==vs['pos'] :
        rating=2.5
        return HttpResponse(str(rating))
    if vs['neg']<vs['pos'] and vs['pos']>0.5 and vs['neg']!=0 :
        rating = 4    
        return HttpResponse(str(rating))
    else:
        rating = 3
        return HttpResponse(str(rating))
cnt1=0
sentence1=""
@api_view(['GET'])
def wordcounter(request,sentence): 
    sentence=sentence.replace('#','')  
    sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
    wordlist=sentence.split()
    for word in wordlist:
        if chr(35) in word:
            continue
    cnt=len(wordlist)
    cnt1=cnt
    sentence1=sentence
    word_count = wordcounterModel.objects.create(sentence=sentence1, count=cnt1).save()
    return HttpResponse(str(cnt))
@api_view(http_method_names=['GET','POST'])
def wordcounterView(request):
    if request.method=='GET':
        return wordcounterget(request)
    elif request.method=='POST':
        return wordcounterpost(request)

def wordcounterget(request):
    try:
        data= wordcounterModel.objects.all()
        serializer= wordcounteSerializer(data,many=True)
        return Response(data=serializer.data)
    except ObjectDoesNotExist :
        return Response(status=status.HTTP_404_NOT_FOUND)
#temp=temp_view()
def wordcounterpost(request):
    #count=request.count
    hdata = wordcounterModel()
    #hdata=sentence
    word_count = wordcounterModel.objects.get(sentence=sentence1)
    count = word_count.count
    serializer=wordcounteSerializer(hdata,data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)
# def temp(request):
#     return {'sentence':sentence1,'count':cnt1}