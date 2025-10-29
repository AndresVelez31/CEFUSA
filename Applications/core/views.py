
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.http import require_http_methods
from .utils import (
    user_is_admin, 
    user_is_profesor, 
    user_can_access_dashboard,
    user_can_access_payments,
    user_can_access_users,
    user_can_crud,
    get_user_role
)
import json
import re


def landing(request):
    return render(request, 'cefusa_landing.html')

def about_us(request):
    return render(request, 'about_us.html')

@login_required
def home_page(request):
    """
    Main application home page view.
    
    Renders the home page with the main system options.
    Shows different options based on user role:
    - Admin: Can see all options (Users, Payments, Dashboard)
    - Profesor: Can only see Users
    
    Args:
        request (HttpRequest): Django HTTP request object
        
    Returns:
        HttpResponse: Rendered home page with role-based options
        
    Decorators:
        @login_required: Requires user authentication
    """
    # Obtener información del rol del usuario
    user = request.user
    context = {
        'user_role': get_user_role(user),
        'is_admin': user_is_admin(user),
        'is_profesor': user_is_profesor(user),
        'can_access_dashboard': user_can_access_dashboard(user),
        'can_access_payments': user_can_access_payments(user),
        'can_access_users': user_can_access_users(user),
        'can_crud': user_can_crud(user),
    }
    
    return render(request, 'home.html', context)

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
    
    Handles user logout and redirects to landing page.
    Compatible with AJAX requests and traditional navigation.
    
    Args:
        request (HttpRequest): Django HTTP request object
        
    Returns:
        AJAX: JsonResponse with redirect URL
        HTTP: HttpResponseRedirect to landing page
        
    Note:
        Logs out user only if authenticated.
        Redirects to landing page regardless of initial state.
    """
    # Log out if authenticated
    if request.user.is_authenticated:
        logout(request)
    
    # Respond based on request type
    if request.headers.get('Content-Type') == 'application/json':
        # AJAX request: JSON response
        return JsonResponse({
            'success': True, 
            'redirect_url': '/'
        })
    
    # Traditional HTTP request: redirect to landing page
    return redirect('/')


# ==================== PASSWORD RECOVERY UTILITIES ====================

def mask_email(email):
    """
    Mask email address for security display.
    
    Example: john.doe@example.com -> jo******@ex*****.com
    
    Args:
        email (str): Email address to mask
        
    Returns:
        str: Masked email address
    """
    if not email or '@' not in email:
        return "***@***.***"
    
    local, domain = email.split('@')
    
    # Mask local part (show first 2 chars)
    if len(local) <= 2:
        masked_local = '*' * len(local)
    else:
        masked_local = local[:2] + '*' * (len(local) - 2)
    
    # Mask domain (show first 2 chars before dot)
    domain_parts = domain.split('.')
    if len(domain_parts[0]) <= 2:
        masked_domain_name = '*' * len(domain_parts[0])
    else:
        masked_domain_name = domain_parts[0][:2] + '*' * (len(domain_parts[0]) - 2)
    
    masked_domain = masked_domain_name + '.' + '.'.join(domain_parts[1:])
    
    return f"{masked_local}@{masked_domain}"


def validate_password_strength(password):
    """
    Validate password meets security requirements.
    
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    
    Args:
        password (str): Password to validate
        
    Returns:
        tuple: (is_valid: bool, error_message: str)
    """
    if len(password) < 8:
        return False, "La contraseña debe tener al menos 8 caracteres."
    
    if not re.search(r'[A-Z]', password):
        return False, "La contraseña debe contener al menos una letra mayúscula."
    
    if not re.search(r'[a-z]', password):
        return False, "La contraseña debe contener al menos una letra minúscula."
    
    if not re.search(r'\d', password):
        return False, "La contraseña debe contener al menos un número."
    
    return True, ""


# ==================== PASSWORD RECOVERY VIEWS ====================

@require_http_methods(["POST"])
def verify_username(request):
    """
    Verify if username exists and return masked email.
    
    Step 1 of password recovery flow.
    
    Args:
        request (HttpRequest): Django HTTP request with username in JSON body
        
    Returns:
        JsonResponse: Success with masked email or error
        
    Example Response:
        Success: {'success': True, 'masked_email': 'jo******@ex*****.com', 'session_token': 'temp_token'}
        Error: {'error': 'Usuario no encontrado.'}
    """
    try:
        data = json.loads(request.body)
        username = data.get('username', '').strip()
        
        if not username:
            return JsonResponse({
                'error': 'El nombre de usuario es requerido.'
            }, status=400)
        
        # Check if user exists
        try:
            user = User.objects.get(username=username)
            
            # Check if user has email
            if not user.email:
                return JsonResponse({
                    'error': 'Este usuario no tiene un correo electrónico asociado. Contacte al administrador.'
                }, status=400)
            
            # Store username in session for verification steps
            request.session['password_reset_username'] = username
            request.session['password_reset_step'] = 1
            
            return JsonResponse({
                'success': True,
                'masked_email': mask_email(user.email)
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'Usuario no encontrado.'
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Datos JSON no válidos.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Error del servidor. Intente nuevamente.'
        }, status=500)


@require_http_methods(["POST"])
def verify_email(request):
    """
    Verify if the provided email matches the user's email.
    
    Step 2 of password recovery flow.
    
    Args:
        request (HttpRequest): Django HTTP request with email in JSON body
        
    Returns:
        JsonResponse: Success or error
        
    Security:
        - Requires username to be set in session from step 1
        - Validates session step progression
    """
    try:
        data = json.loads(request.body)
        email = data.get('email', '').strip().lower()
        
        # Verify session has username from step 1
        username = request.session.get('password_reset_username')
        current_step = request.session.get('password_reset_step')
        
        if not username or current_step != 1:
            return JsonResponse({
                'error': 'Sesión inválida. Por favor, inicie el proceso nuevamente.'
            }, status=400)
        
        if not email:
            return JsonResponse({
                'error': 'El correo electrónico es requerido.'
            }, status=400)
        
        try:
            user = User.objects.get(username=username)
            
            # Verify email matches
            if user.email.lower() == email:
                # Update session to allow password reset
                request.session['password_reset_step'] = 2
                
                return JsonResponse({
                    'success': True,
                    'message': 'Correo verificado correctamente.'
                })
            else:
                return JsonResponse({
                    'error': 'El correo electrónico no coincide. Intente nuevamente.'
                }, status=401)
                
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'Sesión expirada. Por favor, inicie el proceso nuevamente.'
            }, status=400)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Datos JSON no válidos.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Error del servidor. Intente nuevamente.'
        }, status=500)


@require_http_methods(["POST"])
def reset_password(request):
    """
    Reset user password after successful verification.
    
    Step 3 of password recovery flow.
    
    Args:
        request (HttpRequest): Django HTTP request with new passwords in JSON body
        
    Returns:
        JsonResponse: Success or error
        
    Security:
        - Requires completed email verification (step 2)
        - Validates password strength
        - Confirms password match
        - Clears session after successful reset
    """
    try:
        data = json.loads(request.body)
        password1 = data.get('password1', '')
        password2 = data.get('password2', '')
        
        # Verify session progression
        username = request.session.get('password_reset_username')
        current_step = request.session.get('password_reset_step')
        
        if not username or current_step != 2:
            return JsonResponse({
                'error': 'Sesión inválida. Por favor, inicie el proceso nuevamente.'
            }, status=400)
        
        # Validate inputs
        if not password1 or not password2:
            return JsonResponse({
                'error': 'Ambas contraseñas son requeridas.'
            }, status=400)
        
        if password1 != password2:
            return JsonResponse({
                'error': 'Las contraseñas no coinciden.'
            }, status=400)
        
        # Validate password strength
        is_valid, error_message = validate_password_strength(password1)
        if not is_valid:
            return JsonResponse({
                'error': error_message
            }, status=400)
        
        try:
            user = User.objects.get(username=username)
            
            # Update password
            user.set_password(password1)
            user.save()
            
            # Clear session data
            request.session.pop('password_reset_username', None)
            request.session.pop('password_reset_step', None)
            
            return JsonResponse({
                'success': True,
                'message': 'Contraseña actualizada correctamente.'
            })
            
        except User.DoesNotExist:
            return JsonResponse({
                'error': 'Usuario no encontrado.'
            }, status=404)
            
    except json.JSONDecodeError:
        return JsonResponse({
            'error': 'Datos JSON no válidos.'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'error': 'Error del servidor. Intente nuevamente.'
        }, status=500)