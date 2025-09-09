from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Applications.core.urls')),
    path('user/', include('Applications.user.urls')),
    path('payment/', include('Applications.payment.urls')),
    path('dashboard/', include('Applications.dashboard.urls')),
]
