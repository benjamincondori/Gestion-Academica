from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.gestion import Gestion
from app import db
from app.forms.gestion_form import *
from app.utils.decorators import role_required

bp = Blueprint('gestion', __name__, url_prefix='/gestiones')

@bp.route('/')
@role_required('Admin')
def listar_gestiones():
    gestiones = Gestion.query.all()
    return render_template('admin/gestion/listar-gestiones.html', gestiones=gestiones)

@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_gestion():
    form = GestionForm()
    if form.validate_on_submit():
        try:
            nueva_gestion = Gestion(gestion=form.gestion.data)
            db.session.add(nueva_gestion)
            db.session.commit()
            flash('Gestión creada exitosamente.', 'success')
            return redirect(url_for('admin.gestion.listar_gestiones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la gestión: {str(e)}', 'error')
    return render_template('admin/gestion/crear-gestion.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_gestion(id):
    gestion = Gestion.query.get_or_404(id)
    form = GestionEditForm(obj=gestion)
    if form.validate_on_submit():
        try:
            gestion.gestion = form.gestion.data
            db.session.commit()
            flash('Gestión actualizada exitosamente.', 'success')
            return redirect(url_for('admin.gestion.listar_gestiones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la gestión: {str(e)}', 'error')

    return render_template('admin/gestion/actualizar-gestion.html', form=form, gestion=gestion)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_gestion(id):
    gestion = Gestion.query.get_or_404(id)
    try:
        db.session.delete(gestion)
        db.session.commit()
        flash('Gestión eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la gestión: {str(e)}', 'error')
    return redirect(url_for('admin.gestion.listar_gestiones'))


