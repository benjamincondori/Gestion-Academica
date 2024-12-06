from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField, FloatField, TextAreaField
from wtforms.validators import DataRequired, NumberRange, Length
from app.models.gestion import Gestion

class CalificacionForm(FlaskForm):
    estudiante_codigo = SelectField('Estudiante', coerce=str, validators=[DataRequired()])
    materia_id = SelectField('Materia', coerce=int, validators=[DataRequired()])
    periodo_id = SelectField('Periodo', coerce=int, validators=[DataRequired()])
    nota = FloatField('Nota', validators=[
        DataRequired(),
        NumberRange(min=0, max=100, message="La nota debe estar entre 0 y 100."),
    ], render_kw={'placeholder': 'Ej. 70.5'})
    descripcion = TextAreaField('Descripción', validators=[
        DataRequired(),
        Length(max=200, message="La descripción no puede exceder los 200 caracteres.")
    ], render_kw={'placeholder': 'Ej. Examen final'})
    submit = SubmitField('Registrar Calificación')

    def __init__(self, *args, **kwargs):
        super(CalificacionForm, self).__init__(*args, **kwargs)
        gestion = Gestion.query.order_by(Gestion.id.desc()).first()
        self.periodo_id.choices = [(p.id, p.nombre) for p in gestion.periodos]




class CalificaionEditForm(CalificacionForm):
    submit = SubmitField('Actualizar')
