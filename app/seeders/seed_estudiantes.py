import random
import string
from enum import unique

import unicodedata
from werkzeug.security import generate_password_hash
from faker import Faker
from datetime import datetime

from app.models.usuario import Usuario
from app.models.estudiante import Estudiante
from app import db

# Instanciamos Faker para generar datos falsos
fake = Faker()

ultimo_id = 0


def set_ultimo_id(id):
    global ultimo_id
    ultimo_id = id


def get_ultimo_id():
    return ultimo_id


# Datos de los estudiantes (misma lista que usamos para crear usuarios)
estudiantes_data = [
    {"codigo": "EST001", "nombre": "Ronal", "apellido_paterno": "Pérez", "apellido_materno": "Portal",
     "cedula_identidad": "12345677",
     "direccion": "Calle Falsa 123", "telefono": "789456123", "fecha_nacimiento": "2000-01-01", "genero": "Masculino"},
    {"codigo": "EST002", "nombre": "Mariana", "apellido_paterno": "López", "apellido_materno": "Garcia",
     "cedula_identidad": "87653321",
     "direccion": "Calle Real 456", "telefono": "987654321", "fecha_nacimiento": "1999-02-10", "genero": "Femenino"},
    {"codigo": "EST003", "nombre": "Carlos", "apellido_paterno": "Vargas", "apellido_materno": "Hernández",
     "cedula_identidad": "11223354",
     "direccion": "Avenida Principal 789", "telefono": "321654987", "fecha_nacimiento": "2001-03-05",
     "genero": "Masculino"},
    {"codigo": "EST004", "nombre": "Ana Luz", "apellido_paterno": "Rodríguez", "apellido_materno": "Lopez",
     "cedula_identidad": "55667688",
     "direccion": "Calle Secundaria 101", "telefono": "654987321", "fecha_nacimiento": "1998-04-15",
     "genero": "Femenino"},
    {"codigo": "EST005", "nombre": "Pedro", "apellido_paterno": "Aguilar", "apellido_materno": "Fernández",
     "cedula_identidad": "99897766",
     "direccion": "Calle Tercera 102", "telefono": "123456789", "fecha_nacimiento": "2002-05-25",
     "genero": "Masculino"},
    {"codigo": "EST006", "nombre": "Lucía", "apellido_paterno": "Villanueva", "apellido_materno": "Paredes",
     "cedula_identidad": "22334655",
     "direccion": "Calle Cuarta 304", "telefono": "789654321", "fecha_nacimiento": "1997-06-30", "genero": "Femenino"},
    {"codigo": "EST007", "nombre": "David", "apellido_paterno": "Garcia", "apellido_materno": "Torres",
     "cedula_identidad": "66758899",
     "direccion": "Calle Quinta 505", "telefono": "456789123", "fecha_nacimiento": "2000-07-20", "genero": "Masculino"},
    {"codigo": "EST008", "nombre": "Maria Elena", "apellido_paterno": "Oquendo", "apellido_materno": "Arauz",
     "cedula_identidad": "44256677",
     "direccion": "Calle Sexta 707", "telefono": "321456789", "fecha_nacimiento": "1999-08-10", "genero": "Femenino"},
    {"codigo": "EST009", "nombre": "Marcos", "apellido_paterno": "Torrez", "apellido_materno": "González",
     "cedula_identidad": "50664433",
     "direccion": "Calle Séptima 808", "telefono": "987123456", "fecha_nacimiento": "2001-09-05",
     "genero": "Masculino"},
    {"codigo": "EST010", "nombre": "Lauren", "apellido_paterno": "Ruiz", "apellido_materno": "Parada",
     "cedula_identidad": "99886855",
     "direccion": "Calle Octava 909", "telefono": "654321987", "fecha_nacimiento": "1998-10-12", "genero": "Femenino"},
    {"codigo": "EST011", "nombre": "Sofía", "apellido_paterno": "Herrera", "apellido_materno": "Vargas",
     "cedula_identidad": "11122233",
     "direccion": "Calle Luna 123", "telefono": "987111222", "fecha_nacimiento": "2000-11-01", "genero": "Femenino"},
    {"codigo": "EST012", "nombre": "Miguel", "apellido_paterno": "Ortega", "apellido_materno": "Mendoza",
     "cedula_identidad": "22233344",
     "direccion": "Avenida Sol 456", "telefono": "987333444", "fecha_nacimiento": "1999-12-15", "genero": "Masculino"},
    {"codigo": "EST013", "nombre": "Isabella", "apellido_paterno": "Castillo", "apellido_materno": "Moreno",
     "cedula_identidad": "33344455",
     "direccion": "Calle Estrella 789", "telefono": "987555666", "fecha_nacimiento": "1998-01-20",
     "genero": "Femenino"},
    {"codigo": "EST014", "nombre": "Sebastián", "apellido_paterno": "Núñez", "apellido_materno": "Paredes",
     "cedula_identidad": "44455566",
     "direccion": "Calle Rayo 321", "telefono": "987777888", "fecha_nacimiento": "2001-02-10", "genero": "Masculino"},
    {"codigo": "EST015", "nombre": "Camila", "apellido_paterno": "Flores", "apellido_materno": "Jiménez",
     "cedula_identidad": "55566677",
     "direccion": "Avenida Cometa 654", "telefono": "987999000", "fecha_nacimiento": "2002-03-05",
     "genero": "Femenino"},
    {"codigo": "EST016", "nombre": "Alejandro", "apellido_paterno": "Ruiz", "apellido_materno": "Fuentes",
     "cedula_identidad": "66677788",
     "direccion": "Calle Arcoiris 987", "telefono": "986111222", "fecha_nacimiento": "1997-04-18",
     "genero": "Masculino"},
    {"codigo": "EST017", "nombre": "Valentina", "apellido_paterno": "Ramos", "apellido_materno": "Álvarez",
     "cedula_identidad": "77788899",
     "direccion": "Calle Neblina 789", "telefono": "986333444", "fecha_nacimiento": "2000-05-10", "genero": "Femenino"},
    {"codigo": "EST018", "nombre": "Daniel", "apellido_paterno": "Vega", "apellido_materno": "Martínez",
     "cedula_identidad": "88899900",
     "direccion": "Avenida Luna Nueva 123", "telefono": "986555666", "fecha_nacimiento": "1999-06-25",
     "genero": "Masculino"},
    {"codigo": "EST019", "nombre": "Martina", "apellido_paterno": "Villalobos", "apellido_materno": "Serrano",
     "cedula_identidad": "99900011",
     "direccion": "Calle Estela 456", "telefono": "986777888", "fecha_nacimiento": "1998-07-30", "genero": "Femenino"},
    {"codigo": "EST020", "nombre": "Gabriel", "apellido_paterno": "Carrillo", "apellido_materno": "Palacios",
     "cedula_identidad": "00011122",
     "direccion": "Calle Aurora 654", "telefono": "986999000", "fecha_nacimiento": "2001-08-15", "genero": "Masculino"},
    {"codigo": "EST021", "nombre": "Juliana", "apellido_paterno": "Cortez", "apellido_materno": "Zambrano",
     "cedula_identidad": "11122244",
     "direccion": "Avenida Horizonte 321", "telefono": "985111222", "fecha_nacimiento": "2002-09-01",
     "genero": "Femenino"},
    {"codigo": "EST022", "nombre": "Fernando", "apellido_paterno": "Pacheco", "apellido_materno": "Márquez",
     "cedula_identidad": "22233355",
     "direccion": "Calle Amanecer 789", "telefono": "985333444", "fecha_nacimiento": "1997-10-20",
     "genero": "Masculino"},
    {"codigo": "EST023", "nombre": "Daniela", "apellido_paterno": "Chávez", "apellido_materno": "Aguilar",
     "cedula_identidad": "33344466",
     "direccion": "Calle Prisma 123", "telefono": "985555666", "fecha_nacimiento": "1999-11-11", "genero": "Femenino"},
    {"codigo": "EST024", "nombre": "Diego", "apellido_paterno": "Alvarado", "apellido_materno": "Espinoza",
     "cedula_identidad": "44455577",
     "direccion": "Calle Brillo 456", "telefono": "985777888", "fecha_nacimiento": "2000-12-05", "genero": "Masculino"},
    {"codigo": "EST025", "nombre": "Antonia", "apellido_paterno": "Padilla", "apellido_materno": "Gómez",
     "cedula_identidad": "55566688",
     "direccion": "Avenida Niebla 789", "telefono": "985999000", "fecha_nacimiento": "1998-01-22",
     "genero": "Femenino"},
    {"codigo": "EST026", "nombre": "Francisco", "apellido_paterno": "Suárez", "apellido_materno": "Pérez",
     "cedula_identidad": "66677799",
     "direccion": "Calle Aurora 321", "telefono": "984111222", "fecha_nacimiento": "2001-02-17", "genero": "Masculino"},
    {"codigo": "EST027", "nombre": "Florencia", "apellido_paterno": "Guzmán", "apellido_materno": "Delgado",
     "cedula_identidad": "77788800",
     "direccion": "Calle Horizonte 654", "telefono": "984333444", "fecha_nacimiento": "1999-03-08",
     "genero": "Femenino"},
    {"codigo": "EST028", "nombre": "Hugo", "apellido_paterno": "Peña", "apellido_materno": "Zapata",
     "cedula_identidad": "88899911",
     "direccion": "Calle Amanecer 987", "telefono": "984555666", "fecha_nacimiento": "2000-04-19",
     "genero": "Masculino"},
    {"codigo": "EST029", "nombre": "Paula", "apellido_paterno": "Mora", "apellido_materno": "Carrera",
     "cedula_identidad": "99900022",
     "direccion": "Calle Bruma 123", "telefono": "984777888", "fecha_nacimiento": "1998-05-30", "genero": "Femenino"},
    {"codigo": "EST030", "nombre": "Joaquín", "apellido_paterno": "Navarro", "apellido_materno": "Salas",
     "cedula_identidad": "00011133",
     "direccion": "Avenida Viento 456", "telefono": "984999000", "fecha_nacimiento": "2002-06-21",
     "genero": "Masculino"},
    {"codigo": "EST031", "nombre": "Gabriel", "apellido_paterno": "Mejía", "apellido_materno": "Ortega",
     "cedula_identidad": "11221133",
     "direccion": "Calle Luna 101", "telefono": "111222333", "fecha_nacimiento": "2003-01-15", "genero": "Masculino"},
    {"codigo": "EST032", "nombre": "Isabel", "apellido_paterno": "Hernández", "apellido_materno": "Cruz",
     "cedula_identidad": "22331144",
     "direccion": "Calle Estrella 202", "telefono": "222333444", "fecha_nacimiento": "2002-02-28",
     "genero": "Femenino"},
    {"codigo": "EST033", "nombre": "Luis", "apellido_paterno": "Morales", "apellido_materno": "Delgado",
     "cedula_identidad": "33442255",
     "direccion": "Avenida Sol 303", "telefono": "333444555", "fecha_nacimiento": "2001-03-22", "genero": "Masculino"},
    {"codigo": "EST034", "nombre": "Valeria", "apellido_paterno": "Navarro", "apellido_materno": "Fuentes",
     "cedula_identidad": "44553366",
     "direccion": "Calle Nube 404", "telefono": "444555666", "fecha_nacimiento": "2000-04-10", "genero": "Femenino"},
    {"codigo": "EST035", "nombre": "Sebastián", "apellido_paterno": "Pacheco", "apellido_materno": "Ruiz",
     "cedula_identidad": "55664477",
     "direccion": "Calle Brisa 505", "telefono": "555666777", "fecha_nacimiento": "1999-05-05", "genero": "Masculino"},
    {"codigo": "EST036", "nombre": "Camila", "apellido_paterno": "Cortés", "apellido_materno": "Espinoza",
     "cedula_identidad": "66775588",
     "direccion": "Calle Lirio 606", "telefono": "666777888", "fecha_nacimiento": "2002-06-12", "genero": "Femenino"},
    {"codigo": "EST037", "nombre": "Alejandro", "apellido_paterno": "Rojas", "apellido_materno": "Peña",
     "cedula_identidad": "77886699",
     "direccion": "Calle Olivo 707", "telefono": "777888999", "fecha_nacimiento": "1998-07-07", "genero": "Masculino"},
    {"codigo": "EST038", "nombre": "Gabriela", "apellido_paterno": "Serrano", "apellido_materno": "Vargas",
     "cedula_identidad": "88997700",
     "direccion": "Avenida Cedro 808", "telefono": "888999000", "fecha_nacimiento": "1997-08-08", "genero": "Femenino"},
    {"codigo": "EST039", "nombre": "Emiliano", "apellido_paterno": "Bravo", "apellido_materno": "Medina",
     "cedula_identidad": "99008811",
     "direccion": "Calle Magnolia 909", "telefono": "999000111", "fecha_nacimiento": "2000-09-18",
     "genero": "Masculino"},
    {"codigo": "EST040", "nombre": "Diana", "apellido_paterno": "Quintero", "apellido_materno": "Saavedra",
     "cedula_identidad": "00112233",
     "direccion": "Calle Sauce 110", "telefono": "000111222", "fecha_nacimiento": "1999-10-20", "genero": "Femenino"},
    {"codigo": "EST041", "nombre": "Javier", "apellido_paterno": "Montes", "apellido_materno": "Ramos",
     "cedula_identidad": "11224455",
     "direccion": "Calle Laurel 111", "telefono": "111222444", "fecha_nacimiento": "2003-11-15", "genero": "Masculino"},
    {"codigo": "EST042", "nombre": "Paula", "apellido_paterno": "Campos", "apellido_materno": "León",
     "cedula_identidad": "22335566",
     "direccion": "Calle Cactus 212", "telefono": "222333555", "fecha_nacimiento": "2002-12-30", "genero": "Femenino"},
    {"codigo": "EST043", "nombre": "Felipe", "apellido_paterno": "Ferrer", "apellido_materno": "Ávila",
     "cedula_identidad": "33446677",
     "direccion": "Avenida Palma 313", "telefono": "333444666", "fecha_nacimiento": "2001-01-08",
     "genero": "Masculino"},
    {"codigo": "EST044", "nombre": "Adriana", "apellido_paterno": "Muñoz", "apellido_materno": "Gallegos",
     "cedula_identidad": "44557788",
     "direccion": "Calle Tulipán 414", "telefono": "444555777", "fecha_nacimiento": "2000-02-22", "genero": "Femenino"},
    {"codigo": "EST045", "nombre": "Nicolás", "apellido_paterno": "Castillo", "apellido_materno": "Vega",
     "cedula_identidad": "55668899",
     "direccion": "Calle Viento 515", "telefono": "555666888", "fecha_nacimiento": "1999-03-10", "genero": "Masculino"},
    {"codigo": "EST046", "nombre": "Lorena", "apellido_paterno": "Paredes", "apellido_materno": "Aguirre",
     "cedula_identidad": "66779900",
     "direccion": "Calle Amparo 616", "telefono": "666777999", "fecha_nacimiento": "1998-04-15", "genero": "Femenino"},
    {"codigo": "EST047", "nombre": "Santiago", "apellido_paterno": "Arroyo", "apellido_materno": "Mendoza",
     "cedula_identidad": "77880011",
     "direccion": "Avenida Naranjo 717", "telefono": "777888000", "fecha_nacimiento": "2003-05-20",
     "genero": "Masculino"},
    {"codigo": "EST048", "nombre": "Victoria", "apellido_paterno": "Villalobos", "apellido_materno": "Cáceres",
     "cedula_identidad": "88991122",
     "direccion": "Calle Laurel 818", "telefono": "888999111", "fecha_nacimiento": "2002-06-25", "genero": "Femenino"},
    {"codigo": "EST049", "nombre": "Martín", "apellido_paterno": "Reyes", "apellido_materno": "Barrera",
     "cedula_identidad": "99002233",
     "direccion": "Calle Lirio 919", "telefono": "999000222", "fecha_nacimiento": "2001-07-30", "genero": "Masculino"},
    {"codigo": "EST050", "nombre": "Claudia", "apellido_paterno": "Molina", "apellido_materno": "López",
     "cedula_identidad": "00113344",
     "direccion": "Calle Roble 1010", "telefono": "000111333", "fecha_nacimiento": "2000-08-15", "genero": "Femenino"}
]


def seed_usuarios_estudiantes():
    # Crear usuarios a partir de los datos de los estudiantes
    usuarios = []
    ultimo_id = db.session.query(Usuario).order_by(Usuario.id.desc()).first().id
    set_ultimo_id(ultimo_id)
    for i, estudiante in enumerate(estudiantes_data):
        # Eliminar acentos del nombre y apellido
        nombre_sin_acentos = unicodedata.normalize('NFD', estudiante['nombre']).encode('ascii', 'ignore').decode(
            'utf-8')
        apellido_paterno_sin_acentos = unicodedata.normalize('NFD', estudiante['apellido_paterno']).encode('ascii',
                                                                                                           'ignore').decode(
            'utf-8')
        apellido_materno_sin_acentos = unicodedata.normalize('NFD', estudiante['apellido_materno']).encode('ascii',
                                                                                                           'ignore').decode(
            'utf-8')

        # Crear email sin acentos
        email = f"{nombre_sin_acentos.lower()}.{apellido_paterno_sin_acentos.lower()}.{apellido_materno_sin_acentos.lower()}@gmail.com"
        # Usar la cédula de identidad como contraseña
        password = generate_password_hash(estudiante["cedula_identidad"])
        # Crear un usuario con rol de Estudiante
        usuarios.append(Usuario(id=ultimo_id + i + 1, email=email, password=password, rol_id=3))  # Rol de Estudiante

    db.session.add_all(usuarios)
    db.session.commit()

    print("Datos de prueba de la tabla Usuario Estudiantes agregados correctamente.")


def seed_estudiantes():
    # Crear estudiantes vinculados a los usuarios
    estudiantes = []
    ultimo_id = get_ultimo_id()
    for i, estudiante_data in enumerate(estudiantes_data):
        # Asegurar que la fecha de nacimiento tenga el formato correcto (tipo datetime)
        fecha_nacimiento = datetime.strptime(estudiante_data["fecha_nacimiento"], "%Y-%m-%d")
        estudiantes.append(Estudiante(
            codigo=estudiante_data["codigo"],
            nombre=estudiante_data["nombre"],
            apellido_paterno=estudiante_data["apellido_paterno"],
            apellido_materno=estudiante_data["apellido_materno"],
            cedula_identidad=estudiante_data["cedula_identidad"],
            direccion=estudiante_data["direccion"],
            telefono=estudiante_data["telefono"],
            fecha_nacimiento=fecha_nacimiento,
            genero=estudiante_data["genero"],
            usuario_id=ultimo_id + i + 1  # Relacionamos cada estudiante con su usuario
        ))

    db.session.add_all(estudiantes)
    db.session.commit()

    print("Datos de prueba de la tabla Estudiante agregados correctamente.")

# def seed_usuarios_estudiantes():
#     estudiantes_data = []
#     for _ in range(100):  # Generar 100 estudiantes
#         # Datos del estudiante
#         nombre = fake.first_name()
#         apellido_paterno = fake.unique.last_name()
#         apellido_materno = fake.last_name()
#         cedula_identidad = fake.unique.random_int(min=10000000, max=99999999)
#         fecha_nacimiento = fake.date_of_birth(minimum_age=15, maximum_age=20)
#         direccion = fake.address().replace("\n", ", ")
#         telefono = fake.phone_number()[:15]
#         genero = random.choice(["Masculino", "Femenino"])
#
#         # Eliminar acentos de los nombres
#         nombre_sin_acentos = unicodedata.normalize('NFD', nombre).encode('ascii', 'ignore').decode('utf-8')
#         apellido_sin_acentos = unicodedata.normalize('NFD', apellido_paterno).encode('ascii', 'ignore').decode('utf-8')
#
#         # Crear email sin acentos
#         email = f"{nombre_sin_acentos.lower()}.{apellido_sin_acentos.lower()}@gmail.com"
#         password = generate_password_hash(
#             str(cedula_identidad))  # Usar cédula como password (esto debe ser seguro en producción)
#
#         ultimo_id = db.session.query(Usuario).order_by(Usuario.id.desc()).first().id
#
#         # Crear el usuario
#         usuario = Usuario(
#             id=ultimo_id + 1,
#             email=email,
#             password=password,
#             rol_id=3  # Rol de Estudiante
#         )
#
#         db.session.add(usuario)
#         db.session.commit()
#
#         estudiantes_data.append({
#             "codigo": f"EST{str(000 + _ + 1)}",  # Genera códigos como EST001, EST002, etc.
#             "nombre": nombre,
#             "apellido_paterno": apellido_paterno,
#             "apellido_materno": apellido_materno,
#             "cedula_identidad": str(cedula_identidad),
#             "fecha_nacimiento": fecha_nacimiento,
#             "direccion": direccion,
#             "telefono": str(telefono),
#             "genero": genero,
#             "usuario_id": usuario.id  # Relacionar con el ID del usuario
#         })
#
#     # Agregar a la base de datos
#     for estudiante in estudiantes_data:
#         estudiante_obj = Estudiante(
#             codigo=estudiante["codigo"],
#             nombre=estudiante["nombre"],
#             apellido_paterno=estudiante["apellido_paterno"],
#             apellido_materno=estudiante["apellido_materno"],
#             cedula_identidad=estudiante["cedula_identidad"],
#             fecha_nacimiento=estudiante["fecha_nacimiento"],
#             direccion=estudiante["direccion"],
#             telefono=estudiante["telefono"],
#             genero=estudiante["genero"],
#             usuario_id=estudiante["usuario_id"]
#         )
#         db.session.add(estudiante_obj)
#
#     db.session.commit()
#     print("100 estudiantes creados correctamente.")
