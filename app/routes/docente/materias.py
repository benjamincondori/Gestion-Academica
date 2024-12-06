from flask import Blueprint, render_template, g
from app.utils.decorators import role_required

from app import db
from app.models.curso_materia import CursoMateria
from app.models.curso import Curso
from app.models.materia import Materia
from app.models.inscripcion import Inscripcion
from app.models.estudiante import Estudiante

bp = Blueprint('materias', __name__, url_prefix='/materias')


@bp.route('/', methods=['GET', 'POST'])
@role_required('Docente')
def index():
    # Obtener el código del docente autenticado
    docente_codigo = g.usuario.docente.codigo

    # Consultar las materias asociadas al docente
    materias = CursoMateria.query.filter_by(docente_codigo=docente_codigo).all()

    return render_template('docente/materias/listar.html', materias=materias)


@bp.route('/<int:curso_materia_id>', methods=['GET', 'POST'])
@role_required('Docente')
def ver_detalles(curso_materia_id):
    # Consultar el curso-materia
    curso_materia = CursoMateria.query.get_or_404(curso_materia_id)
    curso = Curso.query.get(curso_materia.curso_id)
    materia = Materia.query.get(curso_materia.materia_id)

    # Obtener el código del docente autenticado
    docente_codigo = g.usuario.docente.codigo

    # Obtener los estudiantes inscritos en el curso, filtrando por docente y materia
    estudiantes = obtener_estudiantes(curso.id, docente_codigo, materia.id)

    print("Estudiantes:", estudiantes)

    return render_template('docente/materias/ver-detalles.html',  estudiantes=estudiantes, curso=curso, materia=materia)


def obtener_estudiantes(curso_id, docente_codigo, materia_id):
    # Obtener los estudiantes inscritos en el curso, filtrando por docente y materia
    estudiantes = db.session.query(Estudiante). \
        join(Inscripcion, Estudiante.codigo == Inscripcion.estudiante_codigo). \
        join(CursoMateria, Inscripcion.curso_id == CursoMateria.curso_id). \
        filter(
        Inscripcion.curso_id == curso_id,
        CursoMateria.docente_codigo == docente_codigo,
        CursoMateria.materia_id == materia_id
    ).all()

    return estudiantes

