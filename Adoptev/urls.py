from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('book',views.book),
    path('login',views.login,name="login"),
    path('loginn',views.loginn,name="loginn"),
    path('signnup',views.loginn,name="signnup"),
    path('signup',views.signup, name="signup"),
    path("<phone>/", views.getPhoneNumberRegistered, name="OTP Gen"),

]
