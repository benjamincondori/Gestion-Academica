from app.models.usuario import Usuario
from app.models.rol import Rol
from werkzeug.security import generate_password_hash
from app import db


def seed_roles():
    # Agregar datos de prueba
    admin = Rol(id=1, nombre='Admin')
    docente = Rol(id=2, nombre='Docente')
    estudiante = Rol(id=3, nombre='Estudiante')

    db.session.add_all([admin, docente, estudiante])
    db.session.commit()

    print("Datos de prueba de la tabla Rol agregados correctamente.")


def seed_usuarios():
    # Agregar datos de prueba
    usuario1 = Usuario(id=1, email='admin@gmail.com', password=generate_password_hash('123456'), rol_id=1)

    db.session.add_all([usuario1])
    db.session.commit()

    print("Datos de prueba de la tabla Usuario agregados correctamente.")
