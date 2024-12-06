from app import db

class Paralelo(db.Model):
    __tablename__ = 'paralelos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    # Relación uno a muchos con Curso
    cursos = db.relationship('Curso', back_populates='paralelo', cascade='all, delete-orphan')

    def __repr__(self):
        return f'Paralelo {self.nombre}'