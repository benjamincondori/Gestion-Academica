from flask import Blueprint, render_template, request, url_for, redirect, flash, session, g
from werkzeug.security import check_password_hash

from app.forms.login_form import LoginForm

from app.models.usuario import Usuario

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        # Validando datos
        error = None
        usuario = Usuario.query.filter_by(email=email).first()

        if usuario is None or not check_password_hash(usuario.password, password):
            error = 'Correo o contraseña incorrecta'

        # Iniciando sesion
        if error is None:
            session.clear()
            session['usuario_id'] = usuario.id

            # Redirigiendo según el rol del usuario
            if usuario.rol.nombre == 'Admin':
                return redirect(url_for('admin.home.index'))
            elif usuario.rol.nombre == 'Docente':
                return redirect(url_for('docente.home.index'))
            elif usuario.rol.nombre == 'Estudiante':
                return redirect(url_for('estudiante.home.index'))
            else:
                error = 'Rol no válido'

        flash(error, 'error')

    return render_template('auth/login.html', form=form)


@bp.before_app_request
def load_logged_in_user():
    usuario_id = session.get('usuario_id')

    if usuario_id is None:
        g.usuario = None
    else:
        g.usuario = Usuario.query.get_or_404(usuario_id)


@bp.route('/logout')
def logout():
    session.clear()
    flash('Has cerrado sesión.', 'info')
    return redirect(url_for('auth.login'))
