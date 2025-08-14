from django.urls import path
from . import views

urlpatterns = [
    path('', views.paymentsManagement, name='paymentsManagement'),
    path('pagos/crear/', views.crear_pago, name='crear_pago'),
    path('pagos/gestionar/', views.paymentsManagement, name='gestionar_pagos'),
]