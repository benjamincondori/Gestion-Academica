from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.curso_materia import CursoMateria
from app import db
from app.forms.curso_materia_form import *

from app.utils.decorators import role_required

bp = Blueprint('curso_materia', __name__, url_prefix='/curso_materias')


@bp.route('/')
@role_required('Admin')
def listar_curso_materias():
    curso_materias = CursoMateria.query.all()
    return render_template('admin/curso_materia/listar-curso-materias.html', curso_materias=curso_materias)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_curso_materia():
    form = CursoMateriaForm()
    if form.validate_on_submit():
        try:
            # Validar existencia del curso
            curso = Curso.query.get(form.curso_id.data)
            if curso is None:
                flash('El curso seleccionado no existe.', 'error')
                return render_template('admin/curso_materia/crear-curso-materia.html', form=form)

            # Validar existencia de la materia
            materia = Materia.query.get(form.materia_id.data)
            if materia is None:
                flash('La materia seleccionada no existe.', 'error')
                return render_template('admin/curso_materia/crear-curso-materia.html', form=form)

            # Validar existencia del docente
            docente = Docente.query.filter_by(codigo=form.docente_codigo.data).first()
            if docente is None:
                flash('El docente seleccionado no existe.', 'error')
                return render_template('admin/curso_materia/crear-curso-materia.html', form=form)

            # Verificar si ya existe una asignación para este curso, materia y docente
            asignacion_existente = CursoMateria.query.filter_by(
                curso_id=form.curso_id.data,
                materia_id=form.materia_id.data,
                docente_codigo=form.docente_codigo.data
            ).first()
            if asignacion_existente:
                flash('El docente ya está asignado a esta materia en el curso seleccionado.', 'error')
                return render_template('admin/curso_materia/crear-curso-materia.html', form=form)

            # Verificar si la materia ya está asignada a otro docente en el mismo curso
            conflicto_asignacion = CursoMateria.query.filter_by(
                curso_id=form.curso_id.data,
                materia_id=form.materia_id.data
            ).first()
            if conflicto_asignacion:
                flash(f'La materia "{materia.nombre}" ya está asignada a otro docente en este curso.', 'error')
                return render_template('admin/curso_materia/crear-curso-materia.html', form=form)

            # Crear la nueva asignación
            nuevo_curso_materia = CursoMateria(
                curso_id=form.curso_id.data,
                materia_id=form.materia_id.data,
                docente_codigo=form.docente_codigo.data
            )
            db.session.add(nuevo_curso_materia)
            db.session.commit()
            flash('Docente asignado correctamente.', 'success')
            return redirect(url_for('admin.curso_materia.listar_curso_materias'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al asignar al docente: {str(e)}', 'error')
    return render_template('admin/curso_materia/crear-curso-materia.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_curso_materia(id):
    curso_materia = CursoMateria.query.get_or_404(id)
    form = CursoMateriaEditForm(obj=curso_materia)
    if form.validate_on_submit():
        try:
            # Validar existencia del curso
            curso = Curso.query.get(form.curso_id.data)
            if curso is None:
                flash('El curso seleccionado no existe.', 'error')
                return render_template('admin/curso_materia/actualizar-curso-materia.html', form=form,
                                       curso_materia=curso_materia)

            # Validar existencia de la materia
            materia = Materia.query.get(form.materia_id.data)
            if materia is None:
                flash('La materia seleccionada no existe.', 'error')
                return render_template('admin/curso_materia/actualizar-curso-materia.html', form=form,
                                       curso_materia=curso_materia)

            # Validar existencia del docente
            docente = Docente.query.filter_by(codigo=form.docente_codigo.data).first()
            if docente is None:
                flash('El docente seleccionado no existe.', 'error')
                return render_template('admin/curso_materia/actualizar-curso-materia.html', form=form,
                                       curso_materia=curso_materia)

            # Evitar conflictos con otras asignaciones de la misma materia en el mismo curso
            conflicto_asignacion = CursoMateria.query.filter(
                CursoMateria.curso_id == form.curso_id.data,
                CursoMateria.materia_id == form.materia_id.data,
                CursoMateria.id != id  # Excluir la asignación actual
            ).first()
            if conflicto_asignacion:
                flash(f'La materia "{materia.nombre}" ya está asignada a otro docente en este curso.', 'error')
                return render_template('admin/curso_materia/actualizar-curso-materia.html', form=form,
                                       curso_materia=curso_materia)

            # Actualizar los valores
            curso_materia.curso_id = form.curso_id.data
            curso_materia.materia_id = form.materia_id.data
            curso_materia.docente_codigo = form.docente_codigo.data
            db.session.commit()
            flash('Asignación de docente actualizado exitosamente.', 'success')
            return redirect(url_for('admin.curso_materia.listar_curso_materias'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la asignación de docente: {str(e)}', 'error')

    return render_template('admin/curso_materia/actualizar-curso-materia.html', form=form, curso_materia=curso_materia)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_curso_materia(id):
    curso_materia = CursoMateria.query.get_or_404(id)
    try:
        db.session.delete(curso_materia)
        db.session.commit()
        flash('Desasignación de docente exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al desasignar al docente: {str(e)}', 'error')
    return redirect(url_for('admin.curso_materia.listar_curso_materias'))
