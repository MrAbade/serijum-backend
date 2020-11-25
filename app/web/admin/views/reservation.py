from flask import Blueprint, render_template
from os.path import join
from pathlib import Path

BASE_PATH = Path(join('app', 'web', 'admin')).absolute()
TEMPLATE_FOLDER = join(BASE_PATH, 'templates')
STATIC_FOLDER = join(BASE_PATH, 'static')

bp_admin = Blueprint(
    'admin', __name__,
    url_prefix='/admin',
    template_folder=TEMPLATE_FOLDER,
    static_folder=STATIC_FOLDER
)

@bp_admin.route('/', methods=['GET'])
def index():
    return render_template('index.html')