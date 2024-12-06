import os
from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename

from app.models.estudiante import Estudiante
from app.models.usuario import Usuario
from app import db

from app.utils.decorators import role_required

bp = Blueprint('estudiante', __name__, url_prefix='/estudiantes')

@bp.route('/', methods=['GET', 'POST'])
@role_required('Admin')
def listar_estudiantes():
    estudiantes = Estudiante.query.all()
    return render_template('admin/estudiante/listar-estudiantes.html', estudiantes=estudiantes)


@bp.route('/create', methods=['GET', 'POST'])
@role_required('Admin')
def crear_estudiante():
    if request.method == 'POST':
        # Capturar los datos enviados desde el formulario
        nombre = request.form.get('nombre')  # Nombre del estudiante
        apellido_paterno = request.form.get('apellido_paterno')  # Apellido paterno del estudiante
        apellido_materno = request.form.get('apellido_materno')  # Apellido materno del estudiante
        email = request.form.get('email')  # Correo electrónico
        fecha_nacimiento = request.form.get('fecha_nacimiento')  # Fecha de nacimiento
        cedula_identidad = request.form.get('cedula_identidad')  # Cédula de identidad
        direccion = request.form.get('direccion')  # Dirección del estudiante
        telefono = request.form.get('telefono')  # Número de teléfono
        genero = request.form.get('genero')  # Género (Masculino/Femenino)
        foto = request.files['foto']  # URL de la imagen

        # Validar los datos requeridos
        if not nombre or not apellido_paterno or not apellido_materno or not email or not fecha_nacimiento or not cedula_identidad or not direccion or not telefono or not genero:
            # Enviar un mensaje al usuario si faltan campos obligatorios
            flash('Por favor completa todos los campos requeridos.', 'error')
            return redirect(url_for('admin.estudiante.crear_estudiante'))

        # Verificar si el correo electrónico ya está registrado
        usuario_existente = Usuario.query.filter_by(email=email).first()
        if usuario_existente:
            flash('El correo electrónico ya está registrado.', 'error')
            return redirect(url_for('admin.estudiante.crear_estudiante'))

        # Verificar si la cédula de identidad ya está registrada
        estudiante_existente = Estudiante.query.filter_by(cedula_identidad=cedula_identidad).first()
        if estudiante_existente:
            flash('La cédula de identidad ya está registrada.', 'error')
            return redirect(url_for('admin.estudiante.crear_estudiante'))

        try:
            # Crear un nuevo usuario para el estudiante
            nuevo_usuario = Usuario(
                email=email,
                password=generate_password_hash(cedula_identidad),  # Contraseña por defecto es la cédula de identidad
                rol_id=3  # Rol de docente
            )
            db.session.add(nuevo_usuario)  # Añadir a la sesión de la base de datos
            db.session.flush()  # Obtener el ID del usuario recién creado

            # Crear un nuevo docente con el ID del usuario
            codigo_generado = Estudiante.generar_codigo()
            nuevo_estudiante = Estudiante(
                codigo=codigo_generado,
                nombre=nombre,
                apellido_paterno=apellido_paterno,
                apellido_materno=apellido_materno,
                fecha_nacimiento=fecha_nacimiento,
                cedula_identidad=cedula_identidad,
                direccion=direccion,
                telefono=telefono,
                genero=genero,
                usuario_id=nuevo_usuario.id
            )

            # Guardar la foto en la carpeta de imágenes
            if foto:
                foto.save(f'app/static/media/estudiantes/{secure_filename(codigo_generado)}.jpg')
                nuevo_estudiante.imagen_url = f'/media/estudiantes/{secure_filename(codigo_generado)}.jpg'

            db.session.add(nuevo_estudiante)  # Añadir a la sesión de la base de datos
            db.session.commit()  # Confirmar la transacción
            flash('Estudiante creado exitosamente.', 'success')
            return redirect(url_for('admin.estudiante.listar_estudiantes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al crear el estudiante: {str(e)}', 'error')

    # Renderizar la página del formulario para crear un nuevo estudiante
    return render_template('admin/estudiante/crear-estudiante.html')


@bp.route('/update/<string:codigo>', methods=['GET', 'POST'])
@role_required('Admin')
def actualizar_estudiante(codigo):
    # Buscar el docente por su código
    estudiante = Estudiante.query.get_or_404(codigo)

    if request.method == 'POST':
        # Capturar los datos enviados desde el formulario
        nombre = request.form.get('nombre')  # Nombre del estudiante
        apellido_paterno = request.form.get('apellido_paterno')  # Apellido paterno del estudiante
        apellido_materno = request.form.get('apellido_materno')  # Apellido materno del estudiante
        fecha_nacimiento = request.form.get('fecha_nacimiento')  # Fecha de nacimiento
        cedula_identidad = request.form.get('cedula_identidad')  # Cédula de identidad
        direccion = request.form.get('direccion')  # Dirección del estudiante
        telefono = request.form.get('telefono')  # Número de teléfono
        genero = request.form.get('genero')  # Género (Masculino/Femenino)
        foto = request.files['foto']  # URL de la imagen

        # Validar los datos requeridos
        if not nombre or not apellido_paterno or not apellido_materno or not cedula_identidad or not direccion or not telefono or not genero:
            # Enviar un mensaje al usuario si faltan campos obligatorios
            flash('Por favor completa todos los campos requeridos.', 'error')
            return redirect(url_for('admin.estudiante.actualizar_estudiante', estudiante=estudiante.codigo))

        # Verificar si la cédula de identidad ya está registrada
        estudiante_existente = Estudiante.query.filter(Estudiante.codigo != codigo,
                                                 Estudiante.cedula_identidad == cedula_identidad).first()
        if estudiante_existente:
            flash('La cédula de identidad ya está registrada.', 'error')
            return redirect(url_for('admin.estudiante.actualizar_estudiante', codigo=estudiante.codigo))

        try:
            # Actualizar los datos del estudiante
            estudiante.nombre = nombre
            estudiante.apellido_paterno = apellido_paterno
            estudiante.apellido_materno = apellido_materno
            estudiante.fecha_nacimiento = fecha_nacimiento
            estudiante.cedula_identidad = cedula_identidad
            estudiante.direccion = direccion
            estudiante.telefono = telefono
            estudiante.genero = genero

            # Guardar la foto en la carpeta de imágenes
            if foto:
                # Eliminar la foto anterior si existe
                if estudiante.imagen_url:
                    try:
                        os.remove(f'app/static{estudiante.imagen_url}')  # Eliminar la imagen vieja
                    except FileNotFoundError:
                        pass  # Si la imagen no se encuentra, ignoramos el error

                foto.save(f'app/static/media/estudiantes/{secure_filename(estudiante.codigo)}.jpg')
                estudiante.imagen_url = f'/media/estudiantes/{secure_filename(estudiante.codigo)}.jpg'

            # Guardar los cambios en la base de datos
            db.session.commit()
            flash('Datos del docente actualizados correctamente', 'success')
            return redirect(url_for('admin.estudiante.listar_estudiantes'))
        except Exception as e:
            db.session.rollback()
            flash(f'Error al actualizar el estudiante: {str(e)}', 'error')

    # Renderizar la página del formulario para actualizar un estudiante
    return render_template('admin/estudiante/actualizar-estudiante.html', estudiante=estudiante)


@bp.route('/delete/<string:codigo>')
@role_required('Admin')
def eliminar_estudiante(codigo):
    # Buscar el estudiante por su código
    estudiante = Estudiante.query.get_or_404(codigo)

    try:
        # Eliminar la foto del estudiante si existe
        if estudiante.imagen_url:
            try:
                os.remove(f'app/static{estudiante.imagen_url}')  # Eliminar la imagen
            except FileNotFoundError:
                pass  # Si la imagen no se encuentra, ignoramos el error

        # Eliminar el docente de la base de datos
        db.session.delete(estudiante)
        db.session.commit()
        flash('Estudiante eliminado correctamente', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error al eliminar el estudiante: {str(e)}', 'error')

    # Renderizar la página de confirmación de eliminación
    return redirect(url_for('admin.estudiante.listar_estudiantes'))


