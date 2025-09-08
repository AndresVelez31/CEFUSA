from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from . import views

urlpatterns = [
    path('', lambda request: HttpResponseRedirect('/home/' if request.user.is_authenticated else '/login/'), name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_page, name='homePage')
]
