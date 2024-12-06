from flask import Blueprint, render_template, g
from app.utils.decorators import role_required

from app.models.curso_materia import CursoMateria

bp = Blueprint('cursos', __name__, url_prefix='/cursos')


@bp.route('/', methods=['GET', 'POST'])
@role_required('Docente')
def index():
    # Obtener el código del docente autenticado
    docente_codigo = g.usuario.docente.codigo

    # Consultar los cursos asociados al docente
    cursos = CursoMateria.query.filter_by(docente_codigo=docente_codigo).all()

    return render_template('docente/cursos/listar.html', cursos=cursos)


