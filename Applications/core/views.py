from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import json


@login_required
def home_page(request):
    """
    Main application home page view.
    
    Renders the home page with the main system options.
    Requires user authentication.
    
    Args:
        request (HttpRequest): Django HTTP request object
        
    Returns:
        HttpResponse: Rendered home page
        
    Decorators:
        @login_required: Requires user authentication
    """
    return render(request, 'home.html')

def login_view(request):
    """
    System authentication view.
    
    Handles both login form rendering (GET) and credential processing
    via AJAX (POST).
    
    Features:
    - Only allows access to administrator users (staff/superuser)
    - Support for "Remember me" with persistent sessions
    - Credential and permission validation
    - JSON responses for AJAX requests
    
    Args:
        request (HttpRequest): Django HTTP request object
        
    Returns:
        GET: HttpResponse with login template
        POST: JsonResponse with authentication result
        
    Raises:
        JsonResponse with error 400: Invalid JSON data
        JsonResponse with error 401: Invalid credentials
        JsonResponse with error 403: User without administrator permissions
    """
    # Redirect if already authenticated
    if request.user.is_authenticated:
        return redirect('homePage')
    
    if request.method == 'POST':
        # Process AJAX login request
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            remember_me = data.get('remember', False)
        except json.JSONDecodeError:
            return JsonResponse({
                'error': 'Datos JSON no válidos'
            }, status=400)
        
        # Validate required fields
        if not username or not password:
            return JsonResponse({
                'error': 'Usuario y contraseña son obligatorios.'
            }, status=400)
        
        # Authenticate credentials
        user = authenticate(request, username=username, password=password)
        
        if user is not None and user.is_active:
            # Check administrator permissions
            if user.is_staff or user.is_superuser:
                # Start session
                login(request, user)
                
                # Configure session duration based on "Remember me"
                if remember_me:
                    # Persistent session: 30 days
                    request.session.set_expiry(30 * 24 * 60 * 60)
                    request.session['remember_me'] = True
                else:
                    # Temporary session: expires when browser closes
                    request.session.set_expiry(0)
                    request.session['remember_me'] = False
                
                return JsonResponse({
                    'success': True, 
                    'redirect_url': '/home/'
                }, status=200)
            else:
                return JsonResponse({
                    'error': 'Acceso denegado. Se requieren privilegios de administrador.'
                }, status=403)
        else:
            return JsonResponse({
                'error': 'Usuario o contraseña no válidos.'
            }, status=401)
    
    # Render login form for GET requests
    return render(request, 'login.html')

def logout_view(request):
    """
    User logout view.
    
    Handles user logout and redirects to login page.
    Compatible with AJAX requests and traditional navigation.
    
    Args:
        request (HttpRequest): Django HTTP request object
        
    Returns:
        AJAX: JsonResponse with redirect URL
        HTTP: HttpResponseRedirect to login
        
    Note:
        Logs out user only if authenticated.
        Redirects to login regardless of initial state.
    """
    # Log out if authenticated
    if request.user.is_authenticated:
        logout(request)
    
    # Respond based on request type
    if request.headers.get('Content-Type') == 'application/json':
        # AJAX request: JSON response
        return JsonResponse({
            'success': True, 
            'redirect_url': '/login/'
        })
    
    # Traditional HTTP request: redirect
    return redirect('login')