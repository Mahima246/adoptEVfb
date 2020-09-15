from django.contrib import admin
from django.urls import path,include
from . import views

urlpatterns = [
    path('', views.index),
    path('book',views.book),
    path('book2',views.book2),
    path('profile',views.myprofile),
    path('checkout',views.checkout),
    # path('login',views.login,name="login"),
    path('login/',views.loginn,name="loginn"),
    path('signnup/',views.signnup,name="signnup"),
    path('signup',views.signup, name="signup"),
    path('acc/', include('allauth.urls')),
    path('order/',views.order),
    path('myorder',views.myorder),
    path('mytrip',views.mytrip),
    path('myaddress',views.myaddress)
    # path("<phone>/", views.getPhoneNumberRegistered, name="OTP Gen"),

]
