from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
# Create your views here.
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from textblob import TextBlob 

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