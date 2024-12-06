from app import db

class CursoMateria(db.Model):
    __tablename__ = 'curso_materias'

    id = db.Column(db.Integer, primary_key=True)

    # Llaves foráneas
    curso_id = db.Column(db.Integer, db.ForeignKey('cursos.id'), nullable=False)
    materia_id = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    docente_codigo = db.Column(db.String(20), db.ForeignKey('docentes.codigo'), nullable=False)

    # Relaciones
    curso = db.relationship('Curso', back_populates='curso_materias')
    materia = db.relationship('Materia', back_populates='curso_materias')
    docente = db.relationship('Docente', back_populates='curso_materias')

    def __repr__(self):
        return f'CursoMateria {self.id}'

    def __repr__(self):
        return (
            f'CursoMateria('
            f'id={self.id}, '
            f'curso={self.curso.id} - {self.curso.nombre}, '
            f'materia={self.materia.id} - {self.materia.nombre}, '
            f'docente={self.docente.codigo} - {self.docente.nombre} {self.docente.apellido}'
            ')'
        )