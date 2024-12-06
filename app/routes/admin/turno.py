from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.turno import Turno
from app import db
from app.forms.turno_form import *
from app.utils.decorators import role_required

bp = Blueprint('turno', __name__, url_prefix='/turnos')


@bp.route('/')
@role_required('Admin')
def listar_turnos():
    turnos = Turno.query.all()
    return render_template('admin/turno/listar-turnos.html', turnos=turnos)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_turno():
    form = TurnoForm()
    if form.validate_on_submit():
        try:
            nuevo_turno = Turno(
                nombre=form.nombre.data,
                hora_inicio=form.hora_inicio.data,
                hora_fin=form.hora_fin.data
            )
            db.session.add(nuevo_turno)
            db.session.commit()
            flash('Turno creado exitosamente.', 'success')
            return redirect(url_for('admin.turno.listar_turnos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el turno: {str(e)}', 'error')
    return render_template('admin/turno/crear-turno.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_turno(id):
    turno = Turno.query.get_or_404(id)
    form = TurnoEditForm(obj=turno)
    if form.validate_on_submit():
        try:
            turno.nombre = form.nombre.data
            turno.hora_inicio = form.hora_inicio.data
            turno.hora_fin = form.hora_fin.data
            db.session.commit()
            flash('Turno actualizado exitosamente.', 'success')
            return redirect(url_for('admin.turno.listar_turnos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el turno: {str(e)}', 'error')

    return render_template('admin/turno/actualizar-turno.html', form=form, turno=turno)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_turno(id):
    turno = Turno.query.get_or_404(id)
    try:
        db.session.delete(turno)
        db.session.commit()
        flash('Turno eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el turno: {str(e)}', 'error')
    return redirect(url_for('admin.turno.listar_turnos'))
