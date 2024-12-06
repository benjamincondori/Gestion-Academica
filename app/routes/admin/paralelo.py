from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.paralelo import Paralelo
from app import db
from app.forms.paralelo_form import *
from app.utils.decorators import role_required

bp = Blueprint('paralelo', __name__, url_prefix='/paralelos')


@bp.route('/')
@role_required('Admin')
def listar_paralelos():
    paralelos = Paralelo.query.all()
    return render_template('admin/paralelo/listar-paralelos.html', paralelos=paralelos)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_paralelo():
    form = ParaleloForm()
    if form.validate_on_submit():
        try:
            nuevo_paralelo = Paralelo(nombre=form.nombre.data)
            db.session.add(nuevo_paralelo)
            db.session.commit()
            flash('Paralelo creado exitosamente.', 'success')
            return redirect(url_for('admin.paralelo.listar_paralelos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el paralelo: {str(e)}', 'error')

    return render_template('admin/paralelo/crear-paralelo.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_paralelo(id):
    paralelo = Paralelo.query.get_or_404(id)
    form = ParaleloForm(obj=paralelo)
    if form.validate_on_submit():
        try:
            paralelo.nombre = form.nombre.data
            db.session.commit()
            flash('Paralelo actualizado exitosamente.', 'success')
            return redirect(url_for('admin.paralelo.listar_paralelos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el paralelo: {str(e)}', 'error')

    return render_template('admin/paralelo/actualizar-paralelo.html', form=form, paralelo=paralelo)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_paralelo(id):
    paralelo = Paralelo.query.get_or_404(id)
    try:
        db.session.delete(paralelo)
        db.session.commit()
        flash('Paralelo eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el paralelo: {str(e)}', 'error')
    return redirect(url_for('admin.paralelo.listar_paralelos'))
