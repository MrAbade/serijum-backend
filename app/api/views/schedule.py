from flask import Blueprint
from flask_jwt_extended import fresh_jwt_required, jwt_required

bp_schedule = Blueprint('schedule', __name__, url_prefix='/api/v1/schedule')


@bp_schedule.route('/<int:user_id>/<int:suite_id>', methods=['POST'])
@fresh_jwt_required
def create(user_id, suite_id):
    ...


@bp_schedule.route('/<int:user_id>', methods=['POST'])
@jwt_required
def find_all(user_id):
    ...


@bp_schedule.route('/<int:user_id>/<int:suite_id>', methods=['GET'])
@jwt_required
def find_one(user_id, suite_id):
    ...

