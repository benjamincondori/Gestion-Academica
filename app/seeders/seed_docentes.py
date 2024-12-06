import unicodedata
from werkzeug.security import generate_password_hash
from app.models.usuario import Usuario
from app.models.docente import Docente
from app import db

# Datos de los docentes (misma lista que usamos para crear usuarios)
docentes_data = [
    {"codigo": "DOC001", "nombre": "Juan", "apellido": "Pérez", "cedula_identidad": "12345678",
     "direccion": "Calle Falsa 123", "telefono": "789456123", "genero": "Masculino"},
    {"codigo": "DOC002", "nombre": "María", "apellido": "Gómez", "cedula_identidad": "87654321",
     "direccion": "Calle Real 456", "telefono": "987654321", "genero": "Femenino"},
    {"codigo": "DOC003", "nombre": "Carlos", "apellido": "López", "cedula_identidad": "11223344",
     "direccion": "Avenida Principal 789", "telefono": "321654987", "genero": "Masculino"},
    {"codigo": "DOC004", "nombre": "Ana", "apellido": "Martínez", "cedula_identidad": "55667788",
     "direccion": "Calle Secundaria 101", "telefono": "654987321", "genero": "Femenino"},
    {"codigo": "DOC005", "nombre": "Pedro", "apellido": "Ramírez", "cedula_identidad": "99887766",
     "direccion": "Calle Tercera 102", "telefono": "123456789", "genero": "Masculino"},
    {"codigo": "DOC006", "nombre": "Lucía", "apellido": "Fernández", "cedula_identidad": "22334455",
     "direccion": "Calle Cuarta 304", "telefono": "789654321", "genero": "Femenino"},
    {"codigo": "DOC007", "nombre": "David", "apellido": "Sánchez", "cedula_identidad": "66778899",
     "direccion": "Calle Quinta 505", "telefono": "456789123", "genero": "Masculino"},
    {"codigo": "DOC008", "nombre": "Elena", "apellido": "Torres", "cedula_identidad": "44556677",
     "direccion": "Calle Sexta 707", "telefono": "321456789", "genero": "Femenino"},
    {"codigo": "DOC009", "nombre": "Mario", "apellido": "Álvarez", "cedula_identidad": "55664433",
     "direccion": "Calle Séptima 808", "telefono": "987123456", "genero": "Masculino"},
    {"codigo": "DOC010", "nombre": "Laura", "apellido": "García", "cedula_identidad": "99886655",
     "direccion": "Calle Octava 909", "telefono": "654321987", "genero": "Femenino"}
]


def seed_usuarios_docentes():
    # Crear usuarios a partir de los datos de los docentes
    usuarios = []
    for i, docente in enumerate(docentes_data):
        # Eliminar acentos del nombre y apellido
        nombre_sin_acentos = unicodedata.normalize('NFD', docente['nombre']).encode('ascii', 'ignore').decode('utf-8')
        apellido_sin_acentos = unicodedata.normalize('NFD', docente['apellido']).encode('ascii', 'ignore').decode(
            'utf-8')

        # Crear email sin acentos
        email = f"{nombre_sin_acentos.lower()}.{apellido_sin_acentos.lower()}@gmail.com"
        # Usar la cédula de identidad como contraseña
        password = generate_password_hash(docente["cedula_identidad"])
        # Crear un usuario con rol de Docente
        usuarios.append(Usuario(id=i + 2, email=email, password=password, rol_id=2))  # Rol de Docente

    db.session.add_all(usuarios)
    db.session.commit()

    print("Datos de prueba de la tabla Usuario Docentes agregados correctamente.")


def seed_docentes():
    # Crear docentes vinculados a los usuarios
    docentes = []
    for i, docente_data in enumerate(docentes_data):
        docentes.append(Docente(
            codigo=docente_data["codigo"],
            nombre=docente_data["nombre"],
            apellido=docente_data["apellido"],
            cedula_identidad=docente_data["cedula_identidad"],
            direccion=docente_data["direccion"],
            telefono=docente_data["telefono"],
            genero=docente_data["genero"],
            imagen_url=None,  # Permitir nulo para el campo imagen_url
            usuario_id=i + 2  # Relacionamos cada docente con su usuario
        ))

    db.session.add_all(docentes)
    db.session.commit()

    print("Datos de prueba de la tabla Docente agregados correctamente.")
