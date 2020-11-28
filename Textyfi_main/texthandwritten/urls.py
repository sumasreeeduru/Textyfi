from django.contrib import admin
from django.urls import path , include
from .views import texthandwritten
from api.views import texthandview

urlpatterns = [
   path('texthandapi/',texthandview,name='texthandapi'),
]