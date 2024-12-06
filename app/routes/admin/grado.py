from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.grado import Grado
from app import db
from app.forms.grado_form import *
from app.utils.decorators import role_required

bp = Blueprint('grado', __name__, url_prefix='/grados')


@bp.route('/')
@role_required('Admin')
def listar_grados():
    grados = Grado.query.all()
    return render_template('admin/grado/listar-grados.html', grados=grados)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_grado():
    form = GradoForm()
    if form.validate_on_submit():
        try:
            nuevo_grado = Grado(nombre=form.nombre.data)
            db.session.add(nuevo_grado)
            db.session.commit()
            flash('Grado creado exitosamente.', 'success')
            return redirect(url_for('admin.grado.listar_grados'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el grado: {str(e)}', 'error')

    return render_template('admin/grado/crear-grado.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_grado(id):
    grado = Grado.query.get_or_404(id)
    form = GradoEditForm(obj=grado)
    if form.validate_on_submit():
        try:
            grado.nombre = form.nombre.data
            db.session.commit()
            flash('Grado actualizado exitosamente.', 'success')
            return redirect(url_for('admin.grado.listar_grados'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el grado: {str(e)}', 'error')

    return render_template('admin/grado/actualizar-grado.html', form=form, grado=grado)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_grado(id):
    grado = Grado.query.get_or_404(id)
    try:
        db.session.delete(grado)
        db.session.commit()
        flash('Grado eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el grado: {str(e)}', 'error')
    return redirect(url_for('admin.grado.listar_grados'))
