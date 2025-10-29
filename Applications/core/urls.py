from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('about/', views.about_us, name='about'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_page, name='homePage'),
    
    # Password recovery endpoints
    path('password-recovery/verify-username/', views.verify_username, name='verify_username'),
    path('password-recovery/verify-email/', views.verify_email, name='verify_email'),
    path('password-recovery/reset-password/', views.reset_password, name='reset_password'),
]
