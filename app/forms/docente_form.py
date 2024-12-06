from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, SelectField, FileField, IntegerField, RadioField, SubmitField
from wtforms.validators import DataRequired, Email, Length, ValidationError, NumberRange
from flask_wtf.file import FileAllowed
from app.models.usuario import Usuario
from app.models.docente import Docente

class DocenteForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    apellido = StringField('Apellido', validators=[DataRequired(), Length(max=100)])
    email = EmailField('Correo Electrónico', validators=[DataRequired(), Email()])
    cedula_identidad = StringField('Cédula de identidad', validators=[DataRequired(), Length(max=15)])
    telefono = StringField('Número telefónico', validators=[DataRequired(), Length(max=15)])
    direccion = StringField('Dirección', validators=[DataRequired(), Length(max=200)])
    foto = FileField('Foto de Perfil', validators=[FileAllowed(['jpg', 'png', 'jpeg'], 'Solo se permiten imágenes')])
    genero = RadioField('Género', choices=[('Femenino', 'Femenino'), ('Masculino', 'Masculino')],
                        validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(DocenteForm, self).__init__(*args, **kwargs)
        self.original_docente = kwargs.get('obj', None)

    def validate_email(self, field):
        if self.original_docente and field.data != self.original_docente.usuario.email:
            usuario = Usuario.query.filter_by(email=field.data).first()
            if usuario:
                raise ValidationError('Este email ya está registrado.')

    def validate_cedula_identidad(self, field):
        if self.original_docente and field.data != self.original_docente.cedula_identidad:
            docente = Docente.query.filter_by(cedula_identidad=field.data).first()
            if docente:
                raise ValidationError('La cédula de identidad ya está registrada')


class DocenteEditForm(DocenteForm):
    submit = SubmitField('Actualizar')


