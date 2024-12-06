from flask_wtf import FlaskForm
from wtforms import StringField, DateField, SelectField
from wtforms.fields.simple import SubmitField
from wtforms.validators import DataRequired, Length
from app.models.gestion import Gestion

class PeriodoForm(FlaskForm):
    nombre = StringField('Nombre', validators=[DataRequired(), Length(min=1, max=50)])
    gestion_id = SelectField('Gestión', coerce=int, validators=[DataRequired()])
    fecha_inicio = DateField('Fecha de Inicio', validators=[DataRequired()], format='%Y-%m-%d')
    fecha_fin = DateField('Fecha de Fin', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(PeriodoForm, self).__init__(*args, **kwargs)
        self.gestion_id.choices = [(g.id, g.gestion) for g in Gestion.query.all()]


class PeriodoEditForm(PeriodoForm):
    submit = SubmitField('Actualizar')


