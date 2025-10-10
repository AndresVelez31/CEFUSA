"""
Utilities for roles handling in CEFUSA
"""

def user_is_admin(user): # In this function, we check if the user is an Admin.
    if not user.is_authenticated:
        return False
    
    # SuperUsers are always admins
    if user.is_superuser:
        return True
        
    # Verify if the users is in the Admin group
    return user.groups.filter(name='Admin').exists()

def user_is_profesor(user): # In this function, we check if the user is a Profesor.

    if not user.is_authenticated:
        return False
        
    # Verificar si está en el grupo Profesor
    return user.groups.filter(name='Profesor').exists()


def user_can_access_dashboard(user):
    """
    Verifica si el usuario puede acceder al dashboard.
    Solo los Admin pueden ver el dashboard.
    """
    return user_is_admin(user)


def user_can_access_payments(user):
    """
    Verifica si el usuario puede acceder a la gestión de pagos.
    Solo los Admin pueden acceder a pagos.
    """
    return user_is_admin(user)


def user_can_access_users(user):
    """
    Verifica si el usuario puede acceder a la gestión de usuarios.
    Tanto Admin como Profesor pueden acceder a usuarios.
    """
    return user_is_admin(user) or user_is_profesor(user)


def user_can_crud(user):
    """
    Verifica si el usuario puede hacer operaciones CRUD (Create, Update, Delete).
    Solo los Admin pueden hacer CRUD.
    
    Args:
        user: Usuario de Django
        
    Returns:
        bool: True if user can do CRUD operations, False otherwise
    """
    return user_is_admin(user)


def user_can_view_only(user):
    """
    Verifica si el usuario solo puede ver (read-only).
    Los Profesores solo pueden ver.
    
    Args:
        user: Usuario de Django
        
    Returns:
        bool: True if user can only view, False otherwise
    """
    return user_is_profesor(user) and not user_is_admin(user)


def get_user_role(user):
    """
    Obtiene el rol del usuario como string.
    
    Args:
        user: Usuario de Django
        
    Returns:
        str: 'Admin', 'Profesor', o 'Sin rol'
    """
    if not user.is_authenticated:
        return 'Sin autenticar'
        
    if user_is_admin(user):
        return 'Admin'
    elif user_is_profesor(user):
        return 'Profesor'
    else:
        return 'Sin rol'