from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import Group
from . import models
# Create your views here.

def signupView(request):
    return render(request, 'customer/signup.html')

def CustomerView(request):
    return render(request, 'customer/customer.html')