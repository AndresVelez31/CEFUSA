from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def paymentsManagement(request):
    return HttpResponse('<h1>Welcome to the Payments Management</h1>')