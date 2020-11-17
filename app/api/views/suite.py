
from flask import Blueprint, current_app
from flask.json import jsonify
from flask_jwt_extended import jwt_required

from ..models import Suites

from ..schemas.suites import SuiteSchema
from ..schemas.categories import CategorySchema

bp_suite = Blueprint('suite', __name__, url_prefix='/api/v1/suite')


@bp_suite.route('/', methods=['GET'])
@jwt_required
def find_all():
    try:
        session = current_app.db.session

        suites_with_categories = session.execute("""
        SELECT categories.name, suites.suite_name, suites.suite_number, suites.suite_description
        FROM suites
        JOIN categories ON suites.category_id=categories.id
        ORDER BY (categories.name)
        """)

        serialized_suites = [
            {key: value for key, value in zip(suites_with_categories.keys(), row)}
            for row in suites_with_categories.fetchall()
        ]

        return jsonify(serialized_suites), 200
    
    except Exception as error:
        print(error)
        return jsonify({'msg': 'Cannot get all suites'}), 400

@bp_suite.route('/<int:suite_id>', methods=['GET'])
@jwt_required
def find_by_id(suite_id):
    ss = SuiteSchema()

    suite = Suites.query.get(suite_id)

    return ss.dump(suite, many=False), 200
