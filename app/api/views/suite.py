from flask import Blueprint
from flask_jwt_extended import jwt_required

bp_suite = Blueprint('suite', __name__, url_prefix='/api/v1/suite')


@bp_suite.route('/', methods=['GET'])
@jwt_required
def find_all():
    ...


@bp_suite.route('/<int:suite_id>', methods=['GET'])
@jwt_required
def find_by_id(suite_id):
    ...
