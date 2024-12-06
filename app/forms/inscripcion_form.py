from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models.curso import Curso
from app.models.estudiante import Estudiante
from app.models.gestion import Gestion

class InscripcionForm(FlaskForm):
    estudiante_codigo = SelectField('Estudiante', coerce=str, validators=[DataRequired()])
    curso_id = SelectField('Curso', coerce=int, validators=[DataRequired()])
    gestion_id = SelectField('Gestión', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(InscripcionForm, self).__init__(*args, **kwargs)
        self.estudiante_codigo.choices = [(e.codigo, e.nombre_completo) for e in Estudiante.query.all()]
        self.curso_id.choices = [(c.id, c.curso_info) for c in Curso.query.all()]
        self.gestion_id.choices = [(g.id, g.gestion) for g in Gestion.query.all()]


class InscripcionEditForm(InscripcionForm):
    submit = SubmitField('Actualizar')
