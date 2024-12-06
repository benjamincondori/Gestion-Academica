from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.materia import Materia
from app import db
from app.forms.materia_form import *
from app.utils.decorators import role_required

bp = Blueprint('materia', __name__, url_prefix='/materias')


@bp.route('/')
@role_required('Admin')
def listar_materias():
    materias = Materia.query.all()
    return render_template('admin/materia/listar-materias.html', materias=materias)

@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_materia():
    form = MateriaForm()
    if form.validate_on_submit():
        try:
            nueva_materia = Materia(
                nombre=form.nombre.data,
                descripcion=form.descripcion.data
            )
            db.session.add(nueva_materia)
            db.session.commit()
            flash('Materia creada exitosamente.', 'success')
            return redirect(url_for('admin.materia.listar_materias'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la materia: {str(e)}', 'error')
    return render_template('admin/materia/crear-materia.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_materia(id):
    materia = Materia.query.get_or_404(id)
    form = MateriaEditForm(obj=materia)
    if form.validate_on_submit():
        try:
            materia.nombre = form.nombre.data
            materia.descripcion = form.descripcion.data
            db.session.commit()
            flash('Materia actualizada exitosamente.', 'success')
            return redirect(url_for('admin.materia.listar_materias'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la materia: {str(e)}', 'error')

    return render_template('admin/materia/actualizar-materia.html', form=form, materia=materia)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_materia(id):
    materia = Materia.query.get_or_404(id)
    try:
        db.session.delete(materia)
        db.session.commit()
        flash('Materia eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la materia: {str(e)}', 'error')
    return redirect(url_for('admin.materia.listar_materias'))

