from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Comprobar si el usuario ha iniciado sesión
            if not current_user.is_authenticated:
                flash("Debes iniciar sesión para realizar esta acción.")
                return redirect(url_for('auth.login'))
            
            # Comprobar si el usuario tiene el rol necesario
            if current_user.role != role:
                flash("No tienes permisos para realizar esta acción.")
                return redirect(url_for('navigation.inicio'))
            
            # Si todo está bien, ejecutar la función
            return f(*args, **kwargs)
        return decorated_function
    return decorator