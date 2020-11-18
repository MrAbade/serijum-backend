from flask import Blueprint, request, current_app, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from ...error_handling import UnauthorizedUser
from ...error_handling import IdWasNotFound

from ..models import Users
from ..models import Categories

bp_category = Blueprint('category', __name__, url_prefix='/api/v1/category')


@bp_category.before_request
@jwt_required
def verify_authorization():
    try:
        user_id = get_jwt_identity()

        user = Users.query.get(user_id)

        if not user.is_admin:
            raise UnauthorizedUser
    except UnauthorizedUser as error:
        print(error)
        return jsonify({'msg': 'User not authorized'}), 401


@bp_category.route('/', methods=['GET'])
def list_all():
    try:
        category_list = Categories.query.all()

        category_without_suites = [
            {'id': category.id, 'name': category.name}
            for category in category_list
        ]

        return jsonify(category_without_suites), 200
    except Exception as error:
        print(error)
        return jsonify({'msg': 'Cannot list all categories'}), 400


@bp_category.route('/', methods=['POST'])
def create_category():
    try:
        session = current_app.db.session

        category_name = request.json.get('name')

        category = Categories(name=category_name)
        session.add(category)
        session.commit()

        return jsonify({'id': category.id, 'name': category.name}), 201

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Make sure your body contain all data to complete the creation of new category'}), 400


@bp_category.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    try:
        session = current_app.db.session
        category = Categories.query.filter_by(id=category_id)

        if not category.first():
            raise IdWasNotFound

        category.delete()
        session.commit()

        return jsonify(), 204

    except IdWasNotFound as error:
        print(error)
        return jsonify({'msg': 'The id passed does not exist'}), 400
