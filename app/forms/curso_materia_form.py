from flask_wtf import FlaskForm
from wtforms import SelectField, SubmitField
from wtforms.validators import DataRequired
from app.models.curso import Curso
from app.models.materia import Materia
from app.models.docente import Docente


class CursoMateriaForm(FlaskForm):
    curso_id = SelectField('Curso', coerce=int, validators=[DataRequired()])
    materia_id = SelectField('Materia', coerce=int, validators=[DataRequired()])
    docente_codigo = SelectField('Docente', coerce=str, validators=[DataRequired()])
    submit = SubmitField('Guardar')

    def __init__(self, *args, **kwargs):
        super(CursoMateriaForm, self).__init__(*args, **kwargs)
        self.curso_id.choices = [(c.id, c.curso_info) for c in Curso.query.all()]
        self.materia_id.choices = [(m.id, m.nombre) for m in Materia.query.all()]
        self.docente_codigo.choices = [(d.codigo, d.nombre_completo) for d in Docente.query.all()]


class CursoMateriaEditForm(CursoMateriaForm):
    submit = SubmitField('Actualizar')
