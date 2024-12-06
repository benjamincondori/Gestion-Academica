from flask import Blueprint, render_template, g
from app.utils.decorators import role_required

from app.models.curso_materia import CursoMateria
from app.models.estudiante import Estudiante
from app.models.inscripcion import Inscripcion
from app.models.curso import Curso
from app import db

bp = Blueprint('estudiantes', __name__, url_prefix='/estudiantes')


@bp.route('/', methods=['GET', 'POST'])
@role_required('Docente')
def index():
    # Obtener el código del docente autenticado
    docente_codigo = g.usuario.docente.codigo

    # Consultar los cursos asociados al docente
    cursos = CursoMateria.query.filter_by(docente_codigo=docente_codigo).all()

    # Obtener los estudiantes de los cursos
    estudiantes = obtener_estudiantes_por_docente(docente_codigo)

    print(estudiantes)

    return render_template('docente/estudiantes/listar.html', estudiantes=estudiantes)


def obtener_estudiantes_por_docente(docente_codigo):
    estudiantes = db.session.query(Estudiante).join(
        Inscripcion, Estudiante.codigo == Inscripcion.estudiante_codigo
    ).join(
        Curso, Inscripcion.curso_id == Curso.id
    ).join(
        CursoMateria, Curso.id == CursoMateria.curso_id
    ).filter(
        CursoMateria.docente_codigo == docente_codigo
    ).all()

    return estudiantes
