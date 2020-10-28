from django.urls import path , include
from . import views


urlpatterns = [
    path('',views.index_view, name="index_view"),
    path('login/', views.login_view, name="login_view"),
    path('logout/', views.logout_view, name="logout_view"),
    path('register/', views.register_view, name="register_view"),
     ]