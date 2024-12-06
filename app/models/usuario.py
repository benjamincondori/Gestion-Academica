from app import db


class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    rol_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)

    # Relación con roles
    rol = db.relationship('Rol', back_populates='usuarios')

    # Relación uno a uno con Docente
    docente = db.relationship("Docente", back_populates="usuario", uselist=False)

    # Relación uno a uno con Estudiante
    estudiante = db.relationship("Estudiante", back_populates="usuario", uselist=False)

    def __repr__(self):
        return (
            f'Usuario('
            f'id={self.id}, '
            f'email={self.email}, '
            f'rol={self.rol.name}'
            ')'
        )
