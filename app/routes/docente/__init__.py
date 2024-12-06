from flask import Blueprint

bp = Blueprint('docente', __name__, url_prefix='/docente')


# Importar y registrar las rutas
from .home import bp as home_bp
from .estudiantes import bp as estudiantes_bp
from .materias import bp as materias_bp
from .calificaciones import bp as calificaciones_bp
from .cursos import bp as cursos_bp

# Registrar los Blueprints
bp.register_blueprint(home_bp)
bp.register_blueprint(estudiantes_bp)
bp.register_blueprint(materias_bp)
bp.register_blueprint(calificaciones_bp)
bp.register_blueprint(cursos_bp)


