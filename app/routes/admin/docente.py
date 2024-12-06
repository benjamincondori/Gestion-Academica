import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app.models.docente import Docente
from app.models.usuario import Usuario
from app import db
from app.forms.docente_form import *

from app.utils.decorators import role_required

bp = Blueprint('docente', __name__, url_prefix='/docentes')

@bp.route('/', methods=['GET', 'POST'])
@role_required('Admin')
def listar_docentes():
    docentes = Docente.query.all()
    return render_template('admin/docente/listar-docentes.html', docentes=docentes)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_docente():
    form = DocenteForm()
    if form.validate_on_submit():
        try:
            # Crear un nuevo usuario para el docente
            nuevo_usuario = Usuario(
                email=form.email.data,
                password=generate_password_hash(form.cedula_identidad.data),
                # Contraseña por defecto es la cédula de identidad
                rol_id=2  # Rol de docente
            )
            db.session.add(nuevo_usuario)
            db.session.flush()  # Obtener el ID del usuario recién creado

            # Crear un nuevo docente con el ID del usuario
            codigo_generado = Docente.generar_codigo()
            nuevo_docente = Docente(
                codigo=codigo_generado,
                nombre=form.nombre.data,
                apellido=form.apellido.data,
                cedula_identidad=form.cedula_identidad.data,
                direccion=form.direccion.data,
                telefono=form.telefono.data,
                genero=form.genero.data,
                usuario_id=nuevo_usuario.id
            )

            # Guardar la foto en la carpeta de imágenes
            if form.foto.data:
                filename = secure_filename(f"{codigo_generado}.jpg")
                form.foto.data.save(f'app/static/media/docentes/{filename}')
                nuevo_docente.imagen_url = f'/media/docentes/{filename}'

            db.session.add(nuevo_docente)
            db.session.commit()
            flash('Docente creado exitosamente.', 'success')
            return redirect(url_for('admin.docente.listar_docentes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el docente: {str(e)}', 'error')

    return render_template('admin/docente/crear-docente.html', form=form)



@bp.route('/update/<string:codigo>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_docente(codigo):
    docente = Docente.query.get_or_404(codigo)
    form = DocenteForm(obj=docente)
    form.email.data = docente.usuario.email

    if form.validate_on_submit():
        try:
            docente.nombre = form.nombre.data
            docente.apellido = form.apellido.data
            docente.cedula_identidad = form.cedula_identidad.data
            docente.direccion = form.direccion.data
            docente.telefono = form.telefono.data
            docente.genero = form.genero.data

            if form.foto.data:
                # Eliminar la foto anterior si existe
                if docente.imagen_url:
                    try:
                        os.remove(os.path.join('app', 'static', docente.imagen_url.lstrip('/')))
                    except FileNotFoundError:
                        pass  # Si la imagen no se encuentra, ignoramos el error

                filename = secure_filename(f"{docente.codigo}.jpg")
                form.foto.data.save(os.path.join('app', 'static', 'media', 'docentes', filename))
                docente.imagen_url = f'/media/docentes/{filename}'

            # Guardar los cambios en la base de datos
            db.session.commit()
            flash('Datos del docente actualizados correctamente', 'success')
            return redirect(url_for('admin.docente.listar_docentes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el docente: {str(e)}', 'error')

    # Renderizar la página del formulario para actualizar un docente
    return render_template('admin/docente/actualizar-docente.html', form=form, docente=docente)


@bp.route('/delete/<string:codigo>')
@role_required('Admin')
def eliminar_docente(codigo):
    # Buscar el docente por su código
    docente = Docente.query.get_or_404(codigo)

    try:
        # Eliminar la foto del docente si existe
        if docente.imagen_url:
            try:
                os.remove(f'app/static{docente.imagen_url}')  # Eliminar la imagen
            except FileNotFoundError:
                pass  # Si la imagen no se encuentra, ignoramos el error

        # Eliminar el docente de la base de datos
        db.session.delete(docente)
        db.session.commit()
        flash('Docente eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el docente: {str(e)}', 'error')

    # Renderizar la página de confirmación de eliminación
    return redirect(url_for('admin.docente.listar_docentes'))
