from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class MateriaForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(max=100)])
    descripcion = TextAreaField('Descripción', validators=[Length(max=500)])
    submit = SubmitField('Guardar')

class MateriaEditForm(MateriaForm):
    submit = SubmitField('Actualizar')