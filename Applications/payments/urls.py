from django.urls import path
from . import views

urlpatterns = [
    path('', views.paymentsManagement, name='paymentsManagement'),
    path('pagos/crear/', views.crear_pago, name='crear_pago'),
    path('pagos/gestionar/', views.paymentsManagement, name='gestionar_pagos'),
    path('pagos/<int:pago_id>/edit/', views.edit_pago, name='edit_pago'),
    path('pagos/<int:pago_id>/update/', views.update_pago, name='update_pago'),
]