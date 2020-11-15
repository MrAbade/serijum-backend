from flask import Blueprint
from flask_jwt_extended import jwt_required
from sqlalchemy.orm import joinedload

from ..models import Suites
from ..models import Categories

from ..schemas.suites import SuiteSchema
from ..schemas.categories import CategorySchema

bp_suite = Blueprint('suite', __name__, url_prefix='/api/v1/suite')


@bp_suite.route('/', methods=['GET'])
@jwt_required
def find_all():
    cs = CategorySchema()

    suites_whti_categories = Categories.query.options(joinedload('suites'))
    serialized_suites = cs.dump(suites_whti_categories, many=True)

    return {'suites': serialized_suites}, 200


@bp_suite.route('/<int:suite_id>', methods=['GET'])
@jwt_required
def find_by_id(suite_id):
    ss = SuiteSchema()

    suite = Suites.query.get(suite_id)

    return ss.dump(suite, many=False), 200
