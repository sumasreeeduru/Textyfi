from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
import requests
import json
from rest_framework_simplejwt.tokens import RefreshToken
from .models import user_model
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from api.models import wordcounterModel,ratereviewModel
from api.views import wordcounterView

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
        


# def temp_view(request):
#     return temp
# def wordcounterget(request):
#     try:
#         data=wordcounterModel.objects.all()
#         serializer= wordcounteSerializer(data,many=True)
#         return Response(data=serializer.data)
#     except ObjectDoesNotExist :
#         return Response(status=status.HTTP_404_NOT_FOUND)