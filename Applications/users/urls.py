from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.usersManagement, name='index'),
    path('users/', views.usersManagement, name='usersManagement'),
    path('busqueda-avanzada/', views.busqueda_avanzada, name='busqueda_avanzada'),
    path('acudiente/nuevo/', views.create_acudiente, name='create_acudiente'),
    path('jugador/nuevo/', views.create_jugador, name='create_jugador'),
    path('api/user-details/<str:user_type>/<int:user_id>/', views.get_user_details, name='get_user_details'),
]