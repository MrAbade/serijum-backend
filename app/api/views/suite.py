from flask import Blueprint
from flask_jwt_extended import jwt_required

from ..models import Suites

from ..schemas.suites import SuiteSchema

bp_suite = Blueprint('suite', __name__, url_prefix='/api/v1/suite')


@bp_suite.route('/', methods=['GET'])
@jwt_required
def find_all():
    ss = SuiteSchema()

    suites = Suites.query.all()

    return ss.dump(suites, many=True), 200


@bp_suite.route('/<int:suite_id>', methods=['GET'])
@jwt_required
def find_by_id(suite_id):
    ss = SuiteSchema()

    suite = Suites.query.get(suite_id)

    return ss.dump(suite, many=False), 200
