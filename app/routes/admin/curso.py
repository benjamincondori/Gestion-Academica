from flask import Blueprint, render_template, redirect, url_for, flash
from flask import jsonify

from app.models.curso import Curso
from app import db
from app.forms.curso_form import *
from app.utils.decorators import role_required

bp = Blueprint('curso', __name__, url_prefix='/cursos')


@bp.route('/')
@role_required('Admin')
def listar_cursos():
    cursos = Curso.query.all()
    return render_template('admin/curso/listar-cursos.html', cursos=cursos)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_curso():
    form = CursoForm()
    if form.validate_on_submit():
        try:
            nuevo_curso = Curso(
                nombre=form.nombre.data,
                cupo_maximo=form.cupo_maximo.data,
                turno_id=form.turno_id.data,
                grado_id=form.grado_id.data,
                paralelo_id=form.paralelo_id.data
            )
            db.session.add(nuevo_curso)
            db.session.commit()
            flash('Curso creado exitosamente.', 'success')
            return redirect(url_for('admin.curso.listar_cursos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el curso: {str(e)}', 'error')
    return render_template('admin/curso/crear-curso.html', form=form)

@bp.route('/<int:curso_id>', methods=['GET'])
@role_required('Admin')
def obtener_curso(curso_id):
    curso = Curso.query.get_or_404(curso_id)
    curso_data = {
        'id': curso.id,
        'nombre': curso.nombre,
        'cupo_maximo': curso.cupo_maximo,
        'turno': curso.turno.nombre,
        'grado': curso.grado.nombre,
        'paralelo': curso.paralelo.nombre
    }
    return jsonify(curso_data)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_curso(id):
    curso = Curso.query.get_or_404(id)
    form = CursoEditForm(obj=curso)
    if form.validate_on_submit():
        try:
            curso.nombre = form.nombre.data
            curso.cupo_maximo = form.cupo_maximo.data
            curso.turno_id = form.turno_id.data
            curso.grado_id = form.grado_id.data
            curso.paralelo_id = form.paralelo_id.data
            db.session.commit()
            flash('Curso actualizado exitosamente.', 'success')
            return redirect(url_for('admin.curso.listar_cursos'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el curso: {str(e)}', 'error')

    return render_template('admin/curso/actualizar-curso.html', form=form, curso=curso)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_curso(id):
    curso = Curso.query.get_or_404(id)
    try:
        db.session.delete(curso)
        db.session.commit()
        flash('Curso eliminado exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el curso: {str(e)}', 'error')
    return redirect(url_for('admin.curso.listar_cursos'))
