from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from datetime import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
import pyotp 
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import phoneModel, profile
import base64

# Create your views here.
def index(request):
    return render (request, 'Adoptev/index.html')

def book(request):
    return render (request, 'Adoptev/bookcargo.html')


def book2(request):
    return render (request, 'Adoptev/bookc2.html')

def checkout(request):
    return render(request, 'Adoptev/cashc.html')

def myprofile(request):
    if request.method == 'POST':
        name = request.POST.get('name'),
        Ph_no = request.POST.get('ph-no'),
        email = request.POST.get('email'),
        cname = request.POST.get('cname'),
        gstno = request.POST.get('gstno'),
        address = request.POST.get('address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        profile = profile(name=name, Ph_no=ph_no, email_address = email, company_name = cname, GST_no=gstno, Address= address,city= city, State= state,pincode= pincode)
        profile.save()
    return render (request, 'Adoptev/profile.html')

def myorder(request):
    return render(request, 'Adoptev/orders.html')


def mytrip(request):
    return render(request, 'Adoptev/trip.html')


def myaddress(request):
    return render(request, 'Adoptev/address.html')

def loginn(request):
#     user = authenticate(username='john', password='secret')
#     if user is not None:
#         # A backend authenticated the credentials
#     else:

    return render(request,'Adoptev/login.html')


def signnup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'Adoptev/signup.html')
    # , {'form': form}
    

    # return render(request,'Adoptev/signup.html')
def signup(request):

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = UserCreationForm()
        return render(request, 'signup.html', {'form': form})
    # username = request.POST.get('username')
    # email = request.POST.get('email')
    # password = request.POST.get('password')
    # user = User.objects.create_user(username,email,password)
    # user.save()

    # if request.method =="POST":
    #     form = UserCreationForm(request.POST)
    #     if form.is_valid():
    #         form.save()

    #         return redirect("articles:list")

    # else:
    #     form = UserCreationForm()
    # return render(request,'Adoptev/signup.html',{'form':form})


def order(req):
    return render(req, 'Adoptev/orderdetail.html')

def login(request):
#     if request.method =="POST":
#         form = AuthenticationForm(data=request.POST)
#         if form.is_valid():
#             return redirect('articles')   
#     else:
#         form = AuthenticationForm()
 
    return render(request, 'Adoptev/login.html',{'form':form})  




class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"


class getPhoneNumberRegistered(APIView):
    # Get to Create a call for OTP
    @staticmethod
    def get(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)  # if Mobile already exists the take this else create New One
        except ObjectDoesNotExist:
            phoneModel.objects.create(
                Mobile=phone,
            )
            Mobile = phoneModel.objects.get(Mobile=phone)  # user Newly created Model
        Mobile.counter += 1  # Update Counter At every Call
        Mobile.save()  # Save the data
        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Key is generated
        OTP = pyotp.HOTP(key)  # HOTP Model for OTP is created
        print(OTP.at(Mobile.counter))
        # Using Multi-Threading send the OTP Using Messaging Services like Twilio or Fast2sms
        return Response({"OTP": OTP.at(Mobile.counter)}, status=200)  # Just for demonstration

    # This Method verifies the OTP
    @staticmethod
    def post(request, phone):
        try:
            Mobile = phoneModel.objects.get(Mobile=phone)
        except ObjectDoesNotExist:
            return Response("User does not exist", status=404)  # False Call

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())  # Generating Key
        OTP = pyotp.HOTP(key)  # HOTP Model
        if OTP.verify(request.data["otp"], Mobile.counter):  # Verifying the OTP
            Mobile.isVerified = True
            Mobile.save()
            return Response("You are authorised", status=200)
        return Response("OTP is wrong", status=400)