from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
import requests
import json
from rest_framework_simplejwt.tokens import RefreshToken
from .models import user_model,inpimg
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from api.models import wordcounterModel,ratereviewModel,grammarModel
from api.views import wordcounterView

import re
from django.http import JsonResponse,HttpResponse
import os,io
import pandas as pd
from google.cloud import vision as v
from google.cloud.vision_v1 import types
os.environ['GOOGLE_APPLICATION_CREDENTIALS']=r'app/ServiceAccount.json'
FILE_NAME = 'media/images/2.jpg'
# FOLDER_PATH = r'C:/Users/tanya/Desktop/Textyfi-Copy-Copy/Textyfi_main/app'




def index_view(request):

    return render(request, 'app/index.html')

def register_view(request):
    form = user_model_Form()
    if request.method == 'POST':
        form = user_model_Form(request.POST)
        print(request.POST.get('email'))
        print(request.POST.get('username'))
        print(request.POST.get('password1'))
        print(request.POST.get('password2'))
        print(form.is_valid())
        print(form.errors)
        
        if form.is_valid():
            form.save()
            return redirect('login_view')
    context = {'form': form}
    return render(request, 'app/register.html', context=context)


def login_view(request):
    
    form = AccountAuthenticationForm()
    if request.method == 'POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user = authenticate(request,email=email, password=password)
       
        if user is not None:
            form=login(request,user)
            user=request.user
            user.save()
            
            return redirect('index_view')
    context = {'form': form}
    return render(request, 'app/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')

def ratereview(request):
    rating  = None
    review=ratereviewModel.objects.all()
    if request.method == 'POST':
        res = request.POST
        review = res['review']
        res = requests.get('http://localhost:8000/api/ratereview/' + review)
        rating = res.text

        context = {'rating':rating, 'review':review}
    else:
        context={'rating':0, 'review':'Enter Review'}

    return render(request, 'app/ratereview.html', context)    
# temp={}

def wordcounter(request):
    count=None
    sentence=wordcounterModel.objects.all()
    if request.method == 'POST':
        
        res=request.POST
        sentence=res['sentence']
        res=requests.get('http://localhost:8000/api/wordcounter/'+ sentence)
        count=res.text
        temp={'sentence':sentence,'count':count}
        
    else:
        temp={'sentence':"Enter text", 'count':0}
    return render(request,'app/wordcounter.html',temp)

def grammar(request):
    # grammar="hi"
    text=grammarModel.objects.all()
    if request.method=='POST':
        res=request.POST
        text=res['text']
        res=requests.get('http://localhost:8000/api/grammar/'+ text)

        grammar=res.text
        temp={'text':text,'grammar':grammar}
    else:
        temp={'text':"enter text",'grammar':None}
    return render(request,'app/grammar.html',temp)
    # return HttpResponse(temp)
def wordcounterimg(request):
    if request.method=='POST':
        name1=inpimg(inp_img=request.POST)
        form=imgForm(request.POST,request.FILES)
        if form.is_valid():
            document=form.save(commit=False)
            document.name='2.jpg'
            document.save()
           
            client=v.ImageAnnotatorClient()
            with io.open(FILE_NAME,'rb') as image_file:
                content=image_file.read()
            image=v.Image(content=content)
            response=client.text_detection(image=image)
            texts=response.text_annotations
            df=[]
            for text in texts:
                df.append(text.description
                )
            # df[1:] = [''.join(df[1 : ])] 
            sentence=df[0]
            sentence=sentence.replace('#','')  
            sentence = re.sub(r'[^a-zA-Z0-9\s]', '', sentence)
            wordlist=sentence.split()
            for word in wordlist:
                if chr(35) in word:
                    continue
            cnt=len(wordlist)
            temp={'sentence':sentence,'count':cnt}
            return render(request,'app/wordcounter.html',temp)
    else:
        form=imgForm()
    return render(request,'app/wordcounter.html',{'form':form})
        
