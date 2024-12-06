from app import db

class Periodo(db.Model):
    __tablename__ = 'periodos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    fecha_inicio = db.Column(db.Date, nullable=False)
    fecha_fin = db.Column(db.Date, nullable=False)

    gestion_id = db.Column(db.Integer, db.ForeignKey('gestiones.id'), nullable=False)

    # Relación muchos a uno con Gestion
    gestion = db.relationship('Gestion', back_populates='periodos')

    # Relación uno a muchos con Calificacion
    calificaciones = db.relationship('Calificacion', back_populates='periodo')

    def __repr__(self):
        return f'<Periodo {self.nombre}>'