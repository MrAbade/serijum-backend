from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

from ...error_handling import UnauthorizedUser

from ..models import Users

from ..schemas.categories import CategorySchema

bp_category = Blueprint('category', __name__, url_prefix='/api/v1/category')


@jwt_required
def verify_authorization(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        user_id = get_jwt_identity()

        user = Users.query.get(user_id)

        if not user.is_admin:
            raise UnauthorizedUser
        
        return function(*args, **kwargs)
    return wrapper


@bp_category.route('/', methods=['POST'])
@verify_authorization
def create_category():
    try:
        session = current_app.db.session
        cs = CategorySchema()

        category = cs.load(request.json)
        session.add(category)
        session.commit()

        return cs.dump(session), 201

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Make sure your body contain all data to complete the creation of new category'})
