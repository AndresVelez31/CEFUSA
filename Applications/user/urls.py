from django.urls import path
from . import views
from .views import get_user_details, get_user_edit_form, update_user


urlpatterns = [
    path('', views.display_user, name='index'),
    path('display-user-advanced/', views.display_user_advanced, name='display_user_advanced'),
    path('acudiente/nuevo/', views.create_guardian, name='create_guardian'),
    path('jugador/nuevo/', views.create_player, name='create_player'),
    path('api/user-details/<str:user_type>/<int:user_id>/', views.get_user_details, name='get_user_details'),

    path('get_user_details/<str:user_type>/<int:user_id>/', get_user_details, name='get_user_details'),
    path('edit/form/<str:user_type>/<int:user_id>/', get_user_edit_form, name='get_user_edit_form'),
    path('edit/update/<str:user_type>/<int:user_id>/', update_user, name='update_user'),

    path('delete/<str:user_type>/<int:user_id>/', views.delete_user, name='delete_user'),
]