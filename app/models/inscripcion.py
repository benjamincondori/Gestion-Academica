from app import db
from datetime import datetime

class Inscripcion(db.Model):
    __tablename__ = 'inscripciones'

    id = db.Column(db.Integer, primary_key=True)
    fecha_inscripcion = db.Column(db.DateTime, default=datetime.now())

    # Llaves foráneas
    estudiante_codigo = db.Column(db.String(20), db.ForeignKey('estudiantes.codigo'), nullable=False)
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    gestion_id = db.Column(db.Integer, db.ForeignKey('gestiones.id'), nullable=False)

    # Relaciones
    estudiante = db.relationship('Estudiante', back_populates='inscripciones')
    curso = db.relationship('Curso', back_populates='inscripciones')
    gestion = db.relationship('Gestion', back_populates='inscripciones')

    @property
    def format_fecha_inscripcion(self):
        return self.fecha_inscripcion.strftime('%d/%m/%Y %H:%M:%S %p')

    def __repr__(self):
        return f'Inscripcion {self.id}'