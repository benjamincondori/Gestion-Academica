from flask import Flask
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy

# Instancia de la base de datos
db = SQLAlchemy()

from app.seeders.seed import seed_data

def create_app():
    # Crear aplicacion de Flask
    app = Flask(__name__)

    # Configuracion del proyecto
    app.config.from_object('app.config.Config')

    # Inicializacion de la base de datos
    db.init_app(app)

    # Registrar Blueprints
    from app.routes import home
    app.register_blueprint(home.bp)

    from app.routes.auth import auth
    app.register_blueprint(auth.bp)

    from app.routes.admin import bp as admin_bp
    app.register_blueprint(admin_bp)

    from app.routes.docente import bp as docente_bp
    app.register_blueprint(docente_bp)

    with app.app_context():
        # Crear el esquema de tabla en la base de datos
        from app.models.rol import Rol
        from app.models.usuario import Usuario
        from app.models.docente import Docente
        from app.models.estudiante import Estudiante
        from app.models.gestion import Gestion
        from app.models.turno import Turno
        from app.models.paralelo import Paralelo
        from app.models.grado import Grado
        from app.models.curso import Curso
        from app.models.inscripcion import Inscripcion
        from app.models.materia import Materia
        from app.models.periodo import Periodo
        from app.models.curso_materia import CursoMateria
        from app.models.calificacion import Calificacion

        # db.drop_all()  # Eliminar todas las tablas
        db.create_all()  # Volver a crearlas con los nuevos modelos

        register_cli_commands(app)

    return app


def register_cli_commands(app):
    """
    Registra comandos CLI personalizados para la aplicación.

    Args:
        app (Flask): Instancia de la aplicación Flask.
    """

    @app.cli.command('seed')
    @with_appcontext
    def seed():
        """Comando para ejecutar los seeders."""
        seed_data()
        print("Seeders ejecutados con éxito.")
