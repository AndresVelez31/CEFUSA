from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def usersManagement(request):
    return HttpResponse("<h1>Welcome to Users Management</h1>")