from flask import Blueprint

bp = Blueprint('admin', __name__, url_prefix='/admin')

# Importar y registrar las rutas
from .home import bp as home_bp
from .docente import bp as docente_bp
from .estudiante import bp as estudiante_bp
from .gestion import bp as gestion_bp
from .periodo import bp as periodo_bp
from .grado import bp as grado_bp
from .paralelo import bp as paralelo_bp
from .turno import bp as turno_bp
from .curso import bp as curso_bp
from .inscripcion import bp as inscripcion_bp
from .materia import bp as materia_bp
from .calificacion import bp as calificacion_bp
from .curso_materia import bp as curso_materia_bp

# Registrar los Blueprints
bp.register_blueprint(docente_bp)
bp.register_blueprint(estudiante_bp)
bp.register_blueprint(home_bp)
bp.register_blueprint(gestion_bp)
bp.register_blueprint(periodo_bp)
bp.register_blueprint(grado_bp)
bp.register_blueprint(paralelo_bp)
bp.register_blueprint(turno_bp)
bp.register_blueprint(curso_bp)
bp.register_blueprint(inscripcion_bp)
bp.register_blueprint(materia_bp)
bp.register_blueprint(calificacion_bp)
bp.register_blueprint(curso_materia_bp)

