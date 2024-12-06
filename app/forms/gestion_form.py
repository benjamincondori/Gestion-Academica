from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length


class GestionForm(FlaskForm):
    gestion = StringField('Gestión', validators=[DataRequired(), Length(min=4, max=50)])
    submit = SubmitField('Guardar')


class GestionEditForm(GestionForm):
    submit = SubmitField('Actualizar')
