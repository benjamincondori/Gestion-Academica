from app import db

class Docente(db.Model):
    __tablename__ = 'docentes'
    codigo = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    cedula_identidad = db.Column(db.String(15), nullable=False, unique=True)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relación uno a uno con Usuario
    usuario = db.relationship("Usuario", back_populates="docente", cascade="all")

    # Relación uno a muchos con CursoMateria
    curso_materias = db.relationship('CursoMateria', back_populates='docente')

    def __repr__(self):
        return (
            f'Docente('
            f'codigo={self.codigo}, '
            f'nombre={self.nombre}, '
            f'apellido={self.apellido}, '
            f'genero={self.genero}, '
            f'usuario={self.usuario.email}'
            ')'
        )

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido}'

    @staticmethod
    def generar_codigo():
        """
        Genera un código único para el docente en base al último registro.
        El código tiene el formato 'DOC001', 'DOC002', etc.
        """
        ultimo_docente = Docente.query.order_by(Docente.codigo.desc()).first()
        if ultimo_docente:
            # Extraer la parte numérica del último código y generar el siguiente
            ultimo_codigo = int(ultimo_docente.codigo[3:])  # Suponiendo prefijo "DOC"
            nuevo_codigo = f"DOC{ultimo_codigo + 1:03d}"  # Incrementar y formatear
        else:
            nuevo_codigo = "DOC001"  # Código inicial si no hay registros
        return nuevo_codigo
