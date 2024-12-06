from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class ParaleloForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Guardar')

class ParaleloEditForm(ParaleloForm):
    submit = SubmitField('Actualizar')



