from app import db

class Curso(db.Model):
    __tablename__ = 'cursos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cupo_maximo = db.Column(db.Integer, nullable=False)

    # Claves foráneas
    turno_id = db.Column(db.Integer, db.ForeignKey('turnos.id'), nullable=False)
    grado_id = db.Column(db.Integer, db.ForeignKey('grados.id'), nullable=False)
    paralelo_id = db.Column(db.Integer, db.ForeignKey('paralelos.id'), nullable=False)

    # Relaciones
    turno = db.relationship('Turno', back_populates='cursos')
    grado = db.relationship('Grado', back_populates='cursos')
    paralelo = db.relationship('Paralelo', back_populates='cursos')
    inscripciones = db.relationship('Inscripcion', back_populates='curso')
    curso_materias = db.relationship('CursoMateria', back_populates='curso')

    @property
    def curso_info(self):
        return f'Curso: {self.nombre},  Paralelo: {self.paralelo.nombre},  Turno: {self.turno.nombre}'

    def __repr__(self):
        return f'Curso {self.nombre}'