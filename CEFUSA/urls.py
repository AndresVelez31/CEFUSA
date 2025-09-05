from django.contrib import admin
from django.urls import path
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Applications.core.urls')),
    path('users/', include(('Applications.user.urls', 'user'), namespace='user')),
    path('payments/', include(('Applications.payment.urls', 'payment'), namespace='payment')),
]
