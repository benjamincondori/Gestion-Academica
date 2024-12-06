from app import db

class Grado(db.Model):
    __tablename__ = 'grados'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False, unique=True)

    # Relación uno a muchos con Curso
    cursos = db.relationship('Curso', back_populates='grado')

    def __repr__(self):
        return f'Grado {self.nombre}'