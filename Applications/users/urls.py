from django.urls import path
from . import views
from .views import get_user_details, get_user_edit_form, update_user

app_name = 'users'

urlpatterns = [
    path('', views.usersManagement, name='index'),
    path('users/', views.usersManagement, name='usersManagement'),
    path('busqueda-avanzada/', views.busqueda_avanzada, name='busqueda_avanzada'),
    path('acudiente/nuevo/', views.create_acudiente, name='create_acudiente'),
    path('jugador/nuevo/', views.create_jugador, name='create_jugador'),
    path('api/user-details/<str:user_type>/<int:user_id>/', views.get_user_details, name='get_user_details'),

    path('get_user_details/<str:user_type>/<int:user_id>/', get_user_details, name='get_user_details'),
    path('edit/form/<str:user_type>/<int:user_id>/', get_user_edit_form, name='get_user_edit_form'),
    path('edit/update/<str:user_type>/<int:user_id>/', update_user, name='update_user'),
]