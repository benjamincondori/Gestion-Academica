from app import db

class Materia(db.Model):
    __tablename__ = 'materias'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False, unique=True)
    descripcion = db.Column(db.Text)

    curso_materias = db.relationship('CursoMateria', back_populates='materia')
    calificaciones = db.relationship('Calificacion', back_populates='materia')

    def __repr__(self):
        return f'Materia {self.nombre}'