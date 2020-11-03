from django.urls import path,include
from .views import *
from api.views import wordcounterget
urlpatterns = [
    path('',index_view, name="index_view"),
    path('login/', login_view, name="login_view"),
    path('logout/', logout_view, name="logout_view"),
    path('register/', register_view, name="register_view"),
    path('ratereview/', ratereview, name="ratereview"),
    path('wordcounter/',wordcounter,name='wordcounter'),
    path('wordcounterapi/',wordcounterView,name='wordcounterapi'),
    ]