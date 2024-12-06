import random
from app.models.inscripcion import Inscripcion
from app import db

from app.seeders.seed_cursos import cursos_data
from app.seeders.seed_estudiantes import estudiantes_data
from app.seeders.seed_gestion import gestiones_data

def seed_inscripciones():
    # Crear inscripciones
    inscripciones = []
    total_cursos = len(cursos_data)
    paso = 3  # Salto de 2 en términos de índice (1 + 3 = 4, etc.)

    for estudiante in estudiantes_data:
        # Elegir un índice inicial aleatorio para cursos
        curso_inicio = random.randint(0, total_cursos - (paso * 5))  # Asegura suficientes cursos con saltos

        # Generar una lista de índices con saltos
        indices_cursos = [curso_inicio + i * paso for i in range(5)]

        for i, gestion in enumerate(gestiones_data):
            curso = cursos_data[indices_cursos[i]]  # Toma un curso según los índices generados

            inscripcion = Inscripcion(
                curso_id=curso['id'],
                estudiante_codigo=estudiante['codigo'],
                gestion_id=gestion['id']
            )
            inscripciones.append(inscripcion)

    # Guardar inscripciones en la base de datos
    db.session.add_all(inscripciones)
    db.session.commit()
    print('Inscripciones creadas exitosamente')



