from django.urls import path
from . import views

urlpatterns = [
    path('', views.display_payment, name='display_payment'),
    path('pagos/crear/', views.create_payment, name='create_payment'),
    path('pagos/gestionar/', views.display_payment, name='display_payment'),
    path('pagos/<int:payment_id>/details/', views.get_payment_details, name='get_payment_details'),
    path('pagos/<int:payment_id>/edit/', views.get_payment_edit_form, name='get_payment_edit_form'),
    path('pagos/<int:payment_id>/update/', views.update_payment, name='update_payment'),
    path('pagos/<int:payment_id>/delete/', views.delete_payment, name='delete_payment'),
]