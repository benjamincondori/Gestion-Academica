from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange
from app.models.grado import Grado
from app.models.paralelo import Paralelo
from app.models.turno import Turno

class CursoForm(FlaskForm):
    nombre = StringField(
        'Nombre',
        validators=[DataRequired(), Length(max=100)],
        render_kw={'placeholder': 'Ej. Curso Primero Secundaria'}
    )
    cupo_maximo = IntegerField(
        'Cupo Máximo',
        validators=[DataRequired(), NumberRange(min=1)],
        render_kw={'placeholder': 'Ej. 30'}
    )
    turno_id = SelectField('Turno', coerce=int, validators=[DataRequired()])
    grado_id = SelectField('Grado', coerce=int, validators=[DataRequired()])
    paralelo_id = SelectField('Paralelo', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(CursoForm, self).__init__(*args, **kwargs)
        self.turno_id.choices = [(t.id, t.nombre) for t in Turno.query.all()]
        self.grado_id.choices = [(g.id, g.nombre) for g in Grado.query.all()]
        self.paralelo_id.choices = [(p.id, p.nombre) for p in Paralelo.query.all()]



class CursoEditForm(CursoForm):
    submit = SubmitField('Actualizar')

