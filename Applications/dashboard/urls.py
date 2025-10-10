from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('download-pdf/', views.generate_dashboard_pdf, name='dashboard_pdf'),
    path('download-excel/', views.generate_dashboard_excel, name='dashboard_excel'),
]