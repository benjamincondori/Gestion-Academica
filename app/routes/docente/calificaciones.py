from flask import Blueprint, render_template, request, g, flash, redirect, url_for, jsonify
from sqlalchemy import asc

from app.utils.decorators import role_required

from app import db
from app.models.curso_materia import CursoMateria
from app.models.gestion import Gestion
from app.models.estudiante import Estudiante
from app.models.inscripcion import Inscripcion
from app.models.calificacion import Calificacion
from app.models.materia import Materia

bp = Blueprint('calificaciones', __name__, url_prefix='/calificaciones')


@bp.route('/', methods=['GET', 'POST'])
@role_required('Docente')
def index():
    # Obtener el código del docente autenticado
    docente_codigo = g.usuario.docente.codigo

    # Obtener los estudiantes inscritos en el curso, filtrando por docente y materia
    estudiantes = obtener_estudiantes(docente_codigo)

    # Obtener los periodos de la última gestión
    gestion = Gestion.query.order_by(Gestion.id.desc()).first()
    periodos = gestion.periodos

    return render_template('docente/calificaciones/listar.html', estudiantes=estudiantes, periodos=periodos)


@bp.route('/registrar', methods=['GET', 'POST'])
@role_required('Docente')
def registrar():
    # Obtener el código del docente autenticado
    docente_codigo = g.usuario.docente.codigo

    # Obtener los estudiantes inscritos en el curso, filtrando por docente y materia
    estudiantes = obtener_estudiantes(docente_codigo)

    # Obtener los periodos de la última gestión
    gestion = Gestion.query.order_by(Gestion.id.desc()).first()
    periodos = gestion.periodos

    if request.method == 'POST':
        estudiante_codigo = request.form.get('estudiante_codigo')
        materia_id = request.form.get('materia_id')
        periodo_id = request.form.get('periodo_id')
        nota = request.form.get('nota')
        descripcion = request.form.get('descripcion')

        try:
            # Crear una nueva calificación
            calificacion = Calificacion(
                estudiante_codigo=estudiante_codigo,
                materia_id=materia_id,
                periodo_id=periodo_id,
                nota=nota,
                descripcion=descripcion
            )

            db.session.add(calificacion)
            db.session.commit()

            flash('Calificación registrada correctamente.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'Error al registrar la calificación: {str(e)}', 'error')

    return render_template('docente/calificaciones/registrar.html', estudiantes=estudiantes, periodos=periodos)



@bp.route('/obtener_materias', methods=['GET'])
@role_required('Docente')
def obtener_materias():
    estudiante_codigo = request.args.get('estudiante_codigo')
    docente_codigo = g.usuario.docente.codigo

    if not estudiante_codigo:
        return jsonify({'error': 'Estudiante no proporcionado'}), 400

    # Obtener las materias asociadas al estudiante y al docente
    curso_materias = db.session.query(CursoMateria). \
        join(Inscripcion, CursoMateria.curso_id == Inscripcion.curso_id). \
        filter(
        Inscripcion.estudiante_codigo == estudiante_codigo,
        CursoMateria.docente_codigo == docente_codigo
    ).all()

    # Formatear el resultado
    materias = [{'id': cm.materia_id, 'nombre': cm.materia.nombre} for cm in curso_materias]

    return jsonify(materias)


@bp.route('/consultar_calificaciones', methods=['POST'])
@role_required('Docente')
def consultar_calificaciones():
    estudiante_codigo = request.form.get('estudiante_codigo')
    materia_id = request.form.get('materia_id')
    periodo_id = request.form.get('periodo_id')

    print("Estudiante codigo:" ,estudiante_codigo)
    print("Materia id:" ,materia_id)
    print("Periodo id:" ,periodo_id)

    # Validaciones básicas
    if not estudiante_codigo:
        return jsonify({'error': 'Debe seleccionar un estudiante'}), 400
    if not materia_id:
        return jsonify({'error': 'Debe seleccionar una materia'}), 400
    if not periodo_id:
        return jsonify({'error': 'Debe seleccionar un periodo'}), 400

    # Consulta a la base de datos para obtener las calificaciones
    calificaciones = (
        Calificacion.query
        .filter_by(estudiante_codigo=estudiante_codigo, materia_id=materia_id, periodo_id=periodo_id)
        # .order_by(Calificacion.fecha)  # Opcional, para mostrar cronológicamente
        .all()
    )

    if not calificaciones:
        return jsonify({'error': 'No se encontraron calificaciones para los filtros seleccionados'}), 404

    # Agrupar calificaciones por periodo y calcular promedios
    resultado = {}
    for calificacion in calificaciones:
        periodo = calificacion.periodo.nombre
        if periodo not in resultado:
            resultado[periodo] = {'notas': [], 'promedio': 0}

        resultado[periodo]['notas'].append({
            'id': calificacion.id,
            'nota': calificacion.nota,
            'descripcion': calificacion.descripcion,
        })

    for periodo, datos in resultado.items():
        total_notas = sum(n['nota'] for n in datos['notas'])
        datos['promedio'] = total_notas / len(datos['notas'])

    return jsonify(resultado)


def obtener_estudiantes(docente_codigo):
    # Obtener los estudiantes inscritos en el curso, filtrando por docente y materia
    estudiantes = db.session.query(Estudiante). \
        join(Inscripcion, Estudiante.codigo == Inscripcion.estudiante_codigo). \
        join(CursoMateria, Inscripcion.curso_id == CursoMateria.curso_id). \
        filter(
        CursoMateria.docente_codigo == docente_codigo
    ).order_by(asc(Estudiante.nombre)).all()

    return estudiantes
