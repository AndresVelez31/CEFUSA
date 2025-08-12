from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('', views.usersManagement, name='index'),
    path('users/', views.usersManagement, name='usersManagement'),
    path('busqueda-avanzada/', views.busqueda_avanzada, name='busqueda_avanzada'),
    path('api/user-details/<str:user_type>/<int:user_id>/', views.get_user_details, name='get_user_details'),
    path('<str:user_type>/<int:pk>/edit/', views.get_user_edit_form, name='get_user_edit_form'),
    path('edit/update/<str:user_type>/<int:pk>/', views.update_user, name='update_user'),
]