from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.periodo import Periodo
from app import db
from app.forms.periodo_form import *
from app.utils.decorators import role_required

bp = Blueprint('periodo', __name__, url_prefix='/periodos')


@bp.route('/', methods=['GET', 'POST'])
@role_required('Admin')
def listar_periodos():
    periodos = Periodo.query.all()
    return render_template('admin/periodo/listar-periodos.html', periodos=periodos)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_periodo():
    form = PeriodoForm()
    if form.validate_on_submit():
        try:
            nuevo_periodo = Periodo(
                nombre=form.nombre.data,
                fecha_inicio=form.fecha_inicio.data,
                fecha_fin=form.fecha_fin.data,
                gestion_id=form.gestion_id.data
            )
            db.session.add(nuevo_periodo)
            db.session.commit()
            flash('Periodo creado exitosamente.', 'success')
            return redirect(url_for('admin.periodo.listar_periodos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el periodo: {str(e)}', 'error')
    return render_template('admin/periodo/crear-periodo.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_periodo(id):
    periodo = Periodo.query.get_or_404(id)
    form = PeriodoEditForm(obj=periodo)
    if form.validate_on_submit():
        try:
            periodo.nombre = form.nombre.data
            periodo.fecha_inicio = form.fecha_inicio.data
            periodo.fecha_fin = form.fecha_fin.data
            periodo.gestion_id = form.gestion_id.data
            db.session.commit()
            flash('Periodo actualizado exitosamente.', 'success')
            return redirect(url_for('admin.periodo.listar_periodos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el periodo: {str(e)}', 'error')

    return render_template('admin/periodo/actualizar-periodo.html', form=form, periodo=periodo)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_periodo(id):
    periodo = Periodo.query.get_or_404(id)
    try:
        db.session.delete(periodo)
        db.session.commit()
        flash('Periodo eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el periodo: {str(e)}', 'error')
    return redirect(url_for('admin.periodo.listar_periodos'))


