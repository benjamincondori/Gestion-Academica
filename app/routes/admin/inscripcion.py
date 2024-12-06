from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.inscripcion import Inscripcion
from app import db
from app.forms.inscripcion_form import *
from app.utils.decorators import role_required

bp = Blueprint('inscripcion', __name__, url_prefix='/inscripciones')


@bp.route('/')
@role_required('Admin')
def listar_inscripciones():
    inscripciones = Inscripcion.query.all()
    return render_template('admin/inscripcion/listar-inscripciones.html', inscripciones=inscripciones)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_inscripcion():
    form = InscripcionForm()
    if form.validate_on_submit():
        try:
            # Verificar si el curso existe
            curso = Curso.query.get(form.curso_id.data)
            if curso is None:
                flash('El curso seleccionado no existe.', 'error')
                return render_template('admin/inscripcion/crear-inscripcion.html', form=form)

            # Verificar cupo en el curso
            inscripciones_actuales = Inscripcion.query.filter_by(curso_id=curso.id).count()
            if inscripciones_actuales >= curso.cupo_maximo:
                flash(f'No hay cupo disponible en el curso {curso.nombre}. Cupo máximo: {curso.cupo_maximo}', 'error')
                return render_template('admin/inscripcion/crear-inscripcion.html', form=form)

            # Verificar que el estudiante no esté inscrito en otro curso de la misma gestión
            inscripcion_existente = Inscripcion.query.filter_by(
                estudiante_codigo=form.estudiante_codigo.data,
                gestion_id=form.gestion_id.data
            ).first()
            if inscripcion_existente:
                flash('El estudiante ya está inscrito en otro curso en la misma gestión.', 'error')
                return render_template('admin/inscripcion/crear-inscripcion.html', form=form)

            # Crear la inscripción
            nueva_inscripcion = Inscripcion(
                estudiante_codigo=form.estudiante_codigo.data,
                curso_id=form.curso_id.data,
                gestion_id=form.gestion_id.data
            )
            db.session.add(nueva_inscripcion)
            db.session.commit()
            flash('Inscripción creada exitosamente.', 'success')
            return redirect(url_for('admin.inscripcion.listar_inscripciones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear la inscripción: {str(e)}', 'error')
    return render_template('admin/inscripcion/crear-inscripcion.html', form=form)


@bp.route('/update/<int:id>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_inscripcion(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    form = InscripcionEditForm(obj=inscripcion)
    if form.validate_on_submit():
        try:
            # Obtener el nuevo curso y verificar si existe
            nuevo_curso = Curso.query.get(form.curso_id.data)

            if nuevo_curso is None:
                flash('El curso seleccionado no existe.', 'error')
                return render_template('admin/inscripcion/actualizar-inscripcion.html', form=form,
                                       inscripcion=inscripcion)

            # Validar si el curso es diferente del actual
            if nuevo_curso.id != inscripcion.curso_id:
                # Contar inscripciones en el nuevo curso
                inscripciones_actuales = Inscripcion.query.filter_by(curso_id=nuevo_curso.id).count()

                # Validar cupo
                if inscripciones_actuales >= nuevo_curso.cupo_maximo:
                    flash(
                        f'No hay cupo disponible en el curso {nuevo_curso.nombre}. Cupo máximo: {nuevo_curso.cupo_maximo}',
                        'error')
                    return render_template('admin/inscripcion/actualizar-inscripcion.html', form=form,
                                           inscripcion=inscripcion)

            # Validar que el estudiante no esté inscrito en otro curso en la misma gestión
            inscripcion_existente = Inscripcion.query.filter_by(
                estudiante_codigo=form.estudiante_codigo.data,
                gestion_id=form.gestion_id.data
            ).first()

            if inscripcion_existente and inscripcion_existente.id != inscripcion.id:
                flash('El estudiante ya está inscrito en otro curso en la misma gestión.', 'error')
                return render_template('admin/inscripcion/actualizar-inscripcion.html', form=form,
                                       inscripcion=inscripcion)

            # Actualizar inscripción
            inscripcion.estudiante_codigo = form.estudiante_codigo.data
            inscripcion.curso_id = form.curso_id.data
            inscripcion.gestion_id = form.gestion_id.data
            db.session.commit()
            flash('Inscripción actualizada exitosamente.', 'success')
            return redirect(url_for('admin.inscripcion.listar_inscripciones'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar la inscripción: {str(e)}', 'error')

    return render_template('admin/inscripcion/actualizar-inscripcion.html', form=form, inscripcion=inscripcion)


@bp.route('/delete/<int:id>')
@role_required('Admin')
def eliminar_inscripcion(id):
    inscripcion = Inscripcion.query.get_or_404(id)
    try:
        db.session.delete(inscripcion)
        db.session.commit()
        flash('Inscripción eliminada exitosamente.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar la inscripción: {str(e)}', 'error')
    return redirect(url_for('admin.inscripcion.listar_inscripciones'))
