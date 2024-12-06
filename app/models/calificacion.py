from app import db

class Calificacion(db.Model):
    __tablename__ = 'calificaciones'

    id = db.Column(db.Integer, primary_key=True)
    nota = db.Column(db.Float, nullable=False)
    descripcion = db.Column(db.Text)

    estudiante_codigo = db.Column(db.String(20), db.ForeignKey('estudiantes.codigo'), nullable=False)
    periodo_id = db.Column(db.Integer, db.ForeignKey('periodos.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)

    estudiante = db.relationship('Estudiante', back_populates='calificaciones')
    periodo = db.relationship('Periodo', back_populates='calificaciones')
    materia = db.relationship('Materia', back_populates='calificaciones')

    def __repr__(self):
        return f'Calificacion {self.id}'