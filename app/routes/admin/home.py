from flask import Blueprint, render_template
from app.utils.decorators import role_required

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/', methods=['GET', 'POST'])
@role_required('Admin')
def index():
    return render_template('admin/home.html')