from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from .forms import *
import requests
import json

def index_view(request):
    return render(request, 'app/index.html')

def register_view(request):
    form = user_model_Form()
    if request.method == 'POST':
        form = user_model_Form(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login_view')
    context = {'form': form}
    return render(request, 'app/register.html', context=context)


def login_view(request):
    form = AccountAuthenticationForm()
    if request.method == 'POST':
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect('index_view')
    context = {'form': form}
    return render(request, 'app/login.html', context=context)


def logout_view(request):
    logout(request)
    return redirect('/')

def ratereview(request):
    rating  = None
    if request.method == 'POST':
        res = request.POST
        review = res['review']
        res = requests.get('http://localhost:8000/api/ratereview/' + review)
        rating = res.text

    context = {'rating':rating}

    return render(request, 'app/ratereview.html', context)    

