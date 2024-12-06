from flask import Blueprint, render_template
from app.utils.decorators import role_required

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/', methods=['GET', 'POST'])
@role_required('Docente')
def index():
    return render_template('docente/home.html')