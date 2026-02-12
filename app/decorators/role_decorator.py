from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

# Decorador para verificar el rol del usuario
def role_required(role_name):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Comprobación de seguridad
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para realizar esta acción.")
                return redirect(url_for('auth.login'))
            
            # Comprobación de ROL
            if getattr(current_user, 'rol', None) != role_name:
                flash("No tienes permisos de administrador para ver esto.")
                return redirect(url_for('navigation.inicio'))
            
            # Si todo está bien, adelante
            return f(*args, **kwargs)
        return decorated_function
    return decorator