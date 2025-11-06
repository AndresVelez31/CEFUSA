from django.urls import path
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('home/', views.home_page, name='homePage'),
    
    # Password recovery endpoints
    path('password-recovery/verify-username/', views.verify_username, name='verify_username'),
    path('password-recovery/verify-email/', views.verify_email, name='verify_email'),
    path('password-recovery/reset-password/', views.reset_password, name='reset_password'),

    # Landing page content management (CRUD)
    path('manage-home/', views.manage_landing, name='manage_landing'),
    path('manage-home/edit/', views.edit_landing_page, name='edit_landing_page'),
    path('manage-home/slides/add/', views.create_landing_slide, name='create_landing_slide'),
    path('manage-home/slides/<int:slide_id>/edit/', views.edit_landing_slide, name='edit_landing_slide'),
    path('manage-home/slides/<int:slide_id>/delete/', views.delete_landing_slide, name='delete_landing_slide'),
]
