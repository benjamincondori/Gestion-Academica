from app.seeders.seed_usuarios import seed_roles, seed_usuarios
from app.seeders.seed_gestion import seed_gestion, seed_periodos
from app.seeders.seed_docentes import seed_usuarios_docentes, seed_docentes
from app.seeders.seed_estudiantes import seed_usuarios_estudiantes, seed_estudiantes
from app.seeders.seed_cursos import seed_grados, seed_paralelos, seed_turnos, seed_cursos, seed_curso_materias
from app.seeders.seed_materias import seed_materias
from app.seeders.seed_inscripciones import seed_inscripciones
from app import db

def seed_data():
    # Eliminar todas las tablas
    db.drop_all()
    print("Tablas eliminadas correctamente.")
    print("Creando tablas...")
    db.create_all()
    print("Tablas creadas correctamente.")

    # Ejecutar los seeders
    print("Ejecutando seeders...")
    seed_roles()
    seed_usuarios()
    seed_gestion()
    seed_periodos()
    seed_usuarios_docentes()
    seed_docentes()
    seed_usuarios_estudiantes()
    seed_estudiantes()
    seed_grados()
    seed_paralelos()
    seed_turnos()
    seed_cursos()
    seed_materias()
    seed_curso_materias()
    seed_inscripciones()
    print("Todos los seeders ejecutados correctamente.")
