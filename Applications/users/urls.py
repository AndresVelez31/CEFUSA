from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.usersManagement, name='index'),
    path('users/', views.usersManagement, name='usersManagement'),
    path('busqueda-avanzada/', views.busqueda_avanzada, name='busqueda_avanzada'),
]