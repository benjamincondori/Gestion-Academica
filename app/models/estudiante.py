from app import db

class Estudiante(db.Model):
    __tablename__ = 'estudiantes'
    codigo = db.Column(db.String(20), primary_key=True)
    nombre = db.Column(db.String(120), nullable=False)
    apellido_paterno = db.Column(db.String(50), nullable=False)
    apellido_materno = db.Column(db.String(50), nullable=False)
    fecha_nacimiento = db.Column(db.Date, nullable=False)
    cedula_identidad = db.Column(db.String(15), nullable=False, unique=True)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(15), nullable=False)
    genero = db.Column(db.String(10), nullable=False)
    imagen_url = db.Column(db.String(255), nullable=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)

    # Relación uno a uno con Usuario
    usuario = db.relationship("Usuario", back_populates="estudiante", cascade="all")

    # Relación uno a muchos con Inscripcion
    inscripciones = db.relationship('Inscripcion', back_populates='estudiante')

    # Relación uno a muchos con Calificacion
    calificaciones = db.relationship('Calificacion', back_populates='estudiante')

    def __repr__(self):
        return (
            f'Estudiante('
            f'codigo={self.codigo}, '
            f'nombre={self.nombre}, '
            f'apellido={self.apellido_paterno} {self.apellido_materno}, '
            f'genero={self.genero}, '
            f'usuario={self.usuario.email}'
            ')'
        )

    @property
    def nombre_completo(self):
        return f'{self.nombre} {self.apellido_paterno} {self.apellido_materno}'

    @staticmethod
    def generar_codigo():
        """
        Genera un código único para el estudiante en base al último registro.
        El código tiene el formato 'EST001', 'EST002', etc.
        """
        ultimo_estudiante = Estudiante.query.order_by(Estudiante.codigo.desc()).first()
        if ultimo_estudiante:
            # Extraer la parte numérica del último código y generar el siguiente
            ultimo_codigo = int(ultimo_estudiante.codigo[3:])  # Suponiendo prefijo "EST"
            nuevo_codigo = f"EST{ultimo_codigo + 1:03d}"  # Incrementar y formatear
        else:
            nuevo_codigo = "EST001"  # Código inicial si no hay registros
        return nuevo_codigo

