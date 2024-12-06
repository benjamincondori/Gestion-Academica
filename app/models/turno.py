from app import db


class Turno(db.Model):
    __tablename__ = 'turnos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)
    hora_inicio = db.Column(db.Time, nullable=False)
    hora_fin = db.Column(db.Time, nullable=False)

    # Relación uno a muchos con Curso
    cursos = db.relationship('Curso', back_populates='turno', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Turno {self.nombre}'