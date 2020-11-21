from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta
from os import getenv
from flask_jwt_extended.utils import get_jwt_identity

from ..models import Users

from marshmallow.exceptions import ValidationError
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UniqueViolation
from ...error_handling import UnauthorizedUser

from ..schemas.users import UserSchema

bp_user = Blueprint('users', __name__, url_prefix='/api/v1/user')


@bp_user.route('/login', methods=['POST'])
def login():
    try:
        email = request.json['email']
        password = request.json['password']

        user = Users.query.filter_by(email=email).first()

        if not user or not user.password_verify(password):
            raise UnauthorizedUser()

        access_token = create_access_token(
            identity=user.id, expires_delta=timedelta(days=14))

        us = UserSchema()
        deserialized_user = us.dump(user)

        del deserialized_user['id']
        del deserialized_user['password']
        del deserialized_user['is_admin']
        deserialized_user['access-token'] = access_token

    except KeyError:
        return jsonify({'msg': 'Make sure that valid email and password was passed'}), 400
    except UnauthorizedUser:
        return jsonify({'msg': 'Make sure your password is correct'}), 401

    return deserialized_user, 200


@bp_user.route('/signup', methods=['POST'])
def signup():
    try:
        session = current_app.db.session

        body = {**request.json}
        if body.get('admin_key'):
            del body['admin_key']

        us = UserSchema()
        user = us.load(body, session=session)

        admin_key = request.json.get('admin_key')
        if admin_key == getenv('ADMIN_KEY'):
            user.is_admin = True

        user.gen_hash()
        current_app.db.session.add(user)
        current_app.db.session.commit()

        deserialized_user = us.dump(user)
        del deserialized_user['id']
        del deserialized_user['password']
        del deserialized_user['is_admin']

        return deserialized_user, 201

    except (UniqueViolation, IntegrityError) as error:
        print(error)
        return jsonify({'msg': 'User already exists'}), 400

    except ValidationError as error:
        print(error)
        return jsonify({'msg': 'Some user attributes are missing'}), 400


@bp_user.route('/list', methods=['GET'])
@jwt_required
def list_all_users():
    try:
        user_id = get_jwt_identity()

        admin = Users.query.get(user_id)
        if not admin.is_admin:
            raise UnauthorizedUser

        user_list = Users.query.all()

        get_noadmin_users = [
            {
                'name': user.name,
                'email': user.email
            }
            for user in user_list
            if not user.is_admin
        ]

        return jsonify(get_noadmin_users), 200

    except UnauthorizedUser as error:
        print(error)
        return jsonify({'msg': 'You do not have permission to access this route'}), 401

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Cannot list all users'}), 500 
