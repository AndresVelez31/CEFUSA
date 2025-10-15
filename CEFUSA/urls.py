from django.contrib import admin
from django.urls import path
from django.urls import include
from django.contrib.auth import views as auth_views
from django.shortcuts import redirect

def custom_logout_then_login(request):
    """Custom logout view that redirects to landing page instead of login"""
    from django.contrib.auth import logout
    logout(request)
    return redirect('/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/logout/', custom_logout_then_login, name='admin_logout'),
    path('', include('Applications.core.urls')),
    path('user/', include('Applications.user.urls')),
    path('payment/', include('Applications.payment.urls')),
    path('dashboard/', include('Applications.dashboard.urls')),
]
