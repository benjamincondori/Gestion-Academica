from flask import Blueprint, render_template, redirect, url_for, flash

from app.models.calificacion import Calificacion
from app import db
from app.forms.calificacion_form import *
from app.utils.decorators import role_required

bp = Blueprint('calificacion', __name__, url_prefix='/calificaciones')

@bp.route('/')
@role_required('Admin')
def listar_calificaciones():
    calificaciones = Calificacion.query.all()
    return render_template('admin/calificacion/listar-calificaciones.html', calificaciones=calificaciones)


