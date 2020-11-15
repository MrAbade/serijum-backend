from flask import Blueprint, current_app, request, jsonify
from flask_jwt_extended import create_access_token
from datetime import timedelta

from ..models import Users

from marshmallow.exceptions import ValidationError
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

        us = UserSchema()
        user = us.load(request.json, session=session)

        user.gen_hash()
        current_app.db.session.add(user)
        current_app.db.session.commit()

        deserialized_user = us.dump(user)
        del deserialized_user['id']
        del deserialized_user['password']

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Some user attributes are missing'}), 400

    return deserialized_user, 201
