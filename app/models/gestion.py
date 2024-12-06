from app import db

class Gestion(db.Model):
    __tablename__ = 'gestiones'

    id = db.Column(db.Integer, primary_key=True)
    gestion = db.Column(db.String(50), nullable=False, unique=True)

    # Relación uno a muchos con Periodo y Inscripcion
    periodos = db.relationship('Periodo', back_populates='gestion')
    inscripciones = db.relationship('Inscripcion', back_populates='gestion')

    def __repr__(self):
        return f'Gestion {self.gestion}'