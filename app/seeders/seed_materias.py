from app.models.materia import Materia
from app import db

# Datos de las materias
materias_data = [
    # Materias de Primaria y Secundaria
    {"id": 1, "nombre": "Matemáticas",
     "descripcion": "Materia enfocada en el aprendizaje de conceptos matemáticos."},
    {"id": 2, "nombre": "Lengua Española", "descripcion": "Materia que abarca la gramática, lectura y escritura."},
    {"id": 3, "nombre": "Ciencias Naturales", "descripcion": "Materia que trata sobre biología, física y química."},
    {"id": 4, "nombre": "Historia", "descripcion": "Materia que enseña sobre los eventos históricos importantes."},
    {"id": 5, "nombre": "Geografía",
     "descripcion": "Materia que estudia el planeta, los países, sus características y la geografía."},
    {"id": 6, "nombre": "Educación Física",
     "descripcion": "Materia que promueve la actividad física y el deporte."},
    {"id": 7, "nombre": "Arte",
     "descripcion": "Materia que desarrolla la creatividad y el conocimiento en artes visuales."},
    {"id": 8, "nombre": "Música",
     "descripcion": "Materia que estudia los aspectos teóricos y prácticos de la música."},
    {"id": 9, "nombre": "Inglés", "descripcion": "Materia que enseña el idioma inglés."},
    {"id": 10, "nombre": "Filosofía",
     "descripcion": "Materia que enseña principios filosóficos y pensamiento crítico."},
    {"id": 11, "nombre": "Tecnología",
     "descripcion": "Materia que estudia la tecnología aplicada, informática y robótica."},
]

def seed_materias():
    # Crear materias
    materias = []
    for materia_data in materias_data:
        materias.append(Materia(
            id=materia_data["id"],
            nombre=materia_data["nombre"],
            descripcion=materia_data["descripcion"],
        ))

    db.session.add_all(materias)
    db.session.commit()

    print("Datos de prueba de la tabla Materia agregados correctamente.")
