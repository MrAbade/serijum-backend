from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required

from ..schemas.schedules import ScheduleSchema

from ..models import Schedules


bp_isbusy = Blueprint('isbusy', __name__, url_prefix='/api/v1/isbusy')

@bp_isbusy.route('/<int:suite_id>', methods=['GET'])
@jwt_required
def busy_hours(suite_id):
    try:
        suite_schedules = Schedules.query.filter_by(suite_id=suite_id).all()

        ss = ScheduleSchema()

        return jsonify(ss.dump(suite_schedules, many=True)), 200

    except Exception as error:
        print(error)
        return jsonify({'msg': 'Cannot find busy hours of that suite'}), 400

