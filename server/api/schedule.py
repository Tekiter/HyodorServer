import datetime

from flask_restful import (reqparse, abort, Resource, fields, marshal)

from ..model import User, Schedule
from .. import db
from ..services.login import login_required

from ..services.schedule import (ScheduleResult, get_schedule, create_schedule, delete_schedule)


schedule_field = {
    "id": fields.Integer,
    "type": fields.Integer,
    "content": fields.String,
    "datetime": fields.DateTime(dt_format='iso8601')
}

class ScheduleAPI(Resource):

    @login_required
    def get(self):
        result, sche = get_schedule()

        if result == ScheduleResult.SUCCESS:
            
            output = {
                "schedules": []
            }

            for i in sche:
                output["schedules"].append(marshal(i, schedule_field))

            return output, 200

        return {}, 500


    @login_required
    def post(self):

        parser = reqparse.RequestParser()

        parser.add_argument("type", type=int, required=True)
        parser.add_argument("content", type=str, required=True)
        parser.add_argument("datetime", type=str, required=True)

        args = parser.parse_args()

        try:
            dt = datetime.datetime.fromisoformat(args['datetime'])
        except ValueError:
            return {'message':{'datetime': 'Wrong datetime format. It should be ISO 8601 format.'}}, 400

        sche = Schedule(type=args['type'], content=args['content'], datetime=dt)
        result = create_schedule(sche)

        if result == ScheduleResult.SUCCESS:
            return {}, 201

        return {}, 500


class SchedulePointAPI(Resource):

    @login_required
    def delete(self, schedule_id):
        
        result = delete_schedule(schedule_id)

        if result == ScheduleResult.SUCCESS:
            return {}, 200
        elif result == ScheduleResult.NOT_EXISTS:
            return {'message':'일정이 존재하지 않습니다.'}, 404

        return {}, 500