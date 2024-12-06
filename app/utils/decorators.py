from functools import wraps
from flask import session, redirect, url_for, flash
from app.models.usuario import Usuario

def role_required(*roles):
    """
    Decorador para proteger rutas basado en roles de usuario.

    :param roles: Lista de roles permitidos para acceder a la ruta.
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Verificar si el usuario está autenticado
            usuario_id = session.get('usuario_id')
            if usuario_id is None:
                flash('Por favor, inicia sesión para acceder a esta página.', 'error')
                return redirect(url_for('auth.login'))

            # Verificar el rol del usuario
            usuario = Usuario.query.get(usuario_id)
            if usuario is None or usuario.rol.nombre not in roles:
                flash('No tienes permiso para acceder a esta página.', 'error')
                return redirect(url_for('auth.login'))

            return func(*args, **kwargs)
        return wrapper
    return decorator


