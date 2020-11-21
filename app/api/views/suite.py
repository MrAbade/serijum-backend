
from flask import Blueprint, current_app
from flask.globals import request
from flask.json import jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from sqlalchemy.exc import IntegrityError
from ...error_handling import UnauthorizedUser

from ..models import Suites
from ..models import Users

from ..schemas.suites import SuiteSchema

bp_suite = Blueprint('suite', __name__, url_prefix='/api/v1/suite')


@bp_suite.route('/', methods=['GET'])
@jwt_required
def find_all():
    try:
        session = current_app.db.session

        suites_with_categories = session.execute("""
        SELECT categories.name as category_name, suites.suite_name, suites.suite_number, suites.suite_description
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


@bp_suite.route('/<int:category_id>', methods=['POST'])
@jwt_required
def create_suite(category_id):
    try:
        session = current_app.db.session

        user_id = get_jwt_identity()
        user = Users.query.get(user_id)
        if not user.is_admin:
            raise UnauthorizedUser
        
        suite_attributes = {
            'suite_number': request.json['suite_number'],
            'suite_name': request.json['suite_name'],
            'suite_description': request.json['suite_description'],
            'category_id': category_id
        }

        suite = Suites(**suite_attributes)

        session.add(suite)
        session.commit()

        return SuiteSchema().dump(suite), 200

    except UnauthorizedUser:
        return jsonify({'msg': 'You are not authorized'}), 401

    except IntegrityError:
        return jsonify({'msg': 'The category id does not exist'}), 400
