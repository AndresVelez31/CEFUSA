from django.urls import path
from . import views

urlpatterns = [
    path('payments/', views.paymentsManagement, name='paymentsManagement')
]