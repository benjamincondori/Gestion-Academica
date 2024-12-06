from app import db

class Rol(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)

    # Relación con usuarios
    usuarios = db.relationship('Usuario', back_populates='rol', cascade='all, delete-orphan')

    def __repr__(self) -> str:
        return f'Rol: {self.nombre}'

