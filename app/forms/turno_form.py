from flask_wtf import FlaskForm
from wtforms import StringField, TimeField, SubmitField
from wtforms.validators import DataRequired, Length


class TurnoForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=50)],
        render_kw={'placeholder': 'Ej. Turno Mañana'}
    )
    hora_inicio = TimeField('Hora de Inicio', validators=[DataRequired()])
    hora_fin = TimeField('Hora de Fin', validators=[DataRequired()])
    submit = SubmitField('Guardar')


class TurnoEditForm(TurnoForm):
    submit = SubmitField('Actualizar')


