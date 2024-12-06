import random

from app.models.paralelo import Paralelo
from app.models.turno import Turno
from app.models.grado import Grado
from app.models.curso import Curso
from app.models.curso_materia import CursoMateria
from app import db

from app.seeders.seed_materias import materias_data
from app.seeders.seed_docentes import docentes_data

# Datos de los cursos
cursos_data = [
    # Cursos de Primaria
    {"id": 1, "nombre": "Primero Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 1, "turno_id": 1},
    {"id": 2, "nombre": "Primero Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 2, "turno_id": 1},
    {"id": 3, "nombre": "Primero Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 3, "turno_id": 2},
    {"id": 4, "nombre": "Segundo Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 1, "turno_id": 1},
    {"id": 5, "nombre": "Segundo Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 2, "turno_id": 1},
    {"id": 6, "nombre": "Segundo Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 3, "turno_id": 2},
    {"id": 7, "nombre": "Tercero Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 1, "turno_id": 1},
    {"id": 8, "nombre": "Tercero Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 2, "turno_id": 1},
    {"id": 9, "nombre": "Tercero Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 3, "turno_id": 2},
    {"id": 10, "nombre": "Cuarto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 1, "turno_id": 1},
    {"id": 11, "nombre": "Cuarto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 2, "turno_id": 1},
    {"id": 12, "nombre": "Cuarto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 3, "turno_id": 2},
    {"id": 13, "nombre": "Quinto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 1, "turno_id": 1},
    {"id": 14, "nombre": "Quinto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 2, "turno_id": 1},
    {"id": 15, "nombre": "Quinto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 3, "turno_id": 2},
    {"id": 16, "nombre": "Sexto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 1, "turno_id": 1},
    {"id": 17, "nombre": "Sexto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 2, "turno_id": 1},
    {"id": 18, "nombre": "Sexto Primaria", "cupo_maximo": 30, "grado_id": 1, "paralelo_id": 3, "turno_id": 2},

    # Cursos de Secundaria
    {"id": 19, "nombre": "Primero Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 1, "turno_id": 1},
    {"id": 20, "nombre": "Primero Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 2, "turno_id": 1},
    {"id": 21, "nombre": "Primero Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 3, "turno_id": 2},
    {"id": 22, "nombre": "Segundo Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 1, "turno_id": 1},
    {"id": 23, "nombre": "Segundo Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 2, "turno_id": 2},
    {"id": 24, "nombre": "Segundo Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 3, "turno_id": 3},
    {"id": 25, "nombre": "Tercero Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 1, "turno_id": 1},
    {"id": 26, "nombre": "Tercero Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 2, "turno_id": 1},
    {"id": 27, "nombre": "Tercero Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 3, "turno_id": 2},
    {"id": 28, "nombre": "Cuarto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 1, "turno_id": 1},
    {"id": 29, "nombre": "Cuarto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 2, "turno_id": 2},
    {"id": 30, "nombre": "Cuarto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 3, "turno_id": 3},
    {"id": 31, "nombre": "Quinto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 1, "turno_id": 1},
    {"id": 32, "nombre": "Quinto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 2, "turno_id": 1},
    {"id": 33, "nombre": "Quinto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 3, "turno_id": 2},
    {"id": 34, "nombre": "Sexto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 1, "turno_id": 1},
    {"id": 35, "nombre": "Sexto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 2, "turno_id": 2},
    {"id": 36, "nombre": "Sexto Secundaria", "cupo_maximo": 30, "grado_id": 2, "paralelo_id": 3, "turno_id": 3},
]


def seed_grados():
    # Datos de los grados
    grados_data = [
        {"id": 1, "nombre": "Primaria"},
        {"id": 2, "nombre": "Secundaria"},
    ]

    # Crear grados
    grados = []
    for grado_data in grados_data:
        grados.append(Grado(
            id=grado_data["id"],
            nombre=grado_data["nombre"],
        ))

    db.session.add_all(grados)
    db.session.commit()

    print("Datos de prueba de la tabla Grado agregados correctamente.")


def seed_paralelos():
    # Datos de los paralelos
    paralelos_data = [
        {"id": 1, "nombre": "A"},
        {"id": 2, "nombre": "B"},
        {"id": 3, "nombre": "C"},
    ]

    # Crear paralelos
    paralelos = []
    for paralelo_data in paralelos_data:
        paralelos.append(Paralelo(
            id=paralelo_data["id"],
            nombre=paralelo_data["nombre"],
        ))

    db.session.add_all(paralelos)
    db.session.commit()

    print("Datos de prueba de la tabla Paralelo agregados correctamente.")


def seed_turnos():
    # Datos de los turnos
    turnos_data = [
        {"id": 1, "nombre": "Mañana", "hora_inicio": "07:00:00", "hora_fin": "12:00:00"},
        {"id": 2, "nombre": "Tarde", "hora_inicio": "13:00:00", "hora_fin": "18:00:00"},
        {"id": 3, "nombre": "Noche", "hora_inicio": "19:00:00", "hora_fin": "22:00:00"},
    ]

    # Crear turnos
    turnos = []
    for turno_data in turnos_data:
        turnos.append(Turno(
            id=turno_data["id"],
            nombre=turno_data["nombre"],
            hora_inicio=turno_data["hora_inicio"],
            hora_fin=turno_data["hora_fin"],
        ))

    db.session.add_all(turnos)
    db.session.commit()

    print("Datos de prueba de la tabla Turno agregados correctamente.")


def seed_cursos():
    # Crear cursos
    cursos = []
    for curso_data in cursos_data:
        cursos.append(Curso(
            id=curso_data["id"],
            nombre=curso_data["nombre"],
            cupo_maximo=curso_data["cupo_maximo"],
            grado_id=curso_data["grado_id"],
            paralelo_id=curso_data["paralelo_id"],
            turno_id=curso_data["turno_id"],
        ))

    db.session.add_all(cursos)
    db.session.commit()

    print("Datos de prueba de la tabla Curso agregados correctamente.")


def seed_curso_materias():
    # Crear cursos_materias
    cursos_materias = []
    for curso in cursos_data:
        # Elegir exactamente 2 o 3 materias para cada curso (al azar)
        cantidad_materias = random.randint(1, 2)  # Limitar entre 2 y 3
        materias_seleccionadas = random.sample(materias_data, cantidad_materias)

        for materia in materias_seleccionadas:
            # Elegir un docente aleatorio para cada materia
            docente_seleccionado = random.choice(docentes_data)

            # Crear la relación entre curso, materia y docente
            cursos_materias.append(CursoMateria(
                curso_id=curso["id"],
                materia_id=materia["id"],
                docente_codigo=docente_seleccionado["codigo"],
            ))

    # Guardar las relaciones en la base de datos
    db.session.add_all(cursos_materias)
    db.session.commit()

    print("Datos de prueba de la tabla CursoMateria agregados correctamente.")
