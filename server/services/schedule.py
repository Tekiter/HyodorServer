from sqlalchemy.exc import IntegrityError

from .. import db
from ..model import User, Schedule
from .login import login_required, get_userinfo, get_user, UserPermission


class ScheduleResult:
    SUCCESS = 0
    INTERNAL_ERROR = 30
    NOT_EXISTS = 11
    DB_ERROR = 5
    NOT_OWNER = 12


def get_schedule():
    user = get_user()

    schedules = Schedule.query.filter_by(owner=user)

    return ScheduleResult.SUCCESS, schedules


def create_schedule(schedule: Schedule):
    user = get_user()

    schedule.owner = user

    
    try:
        db.session.add(schedule)
        db.session.commit()
    except:
        return ScheduleResult.INTERNAL_ERROR

    return ScheduleResult.SUCCESS

def delete_schedule(schedule_id):
    sche: Schedule = Schedule.query.get(schedule_id)

    if sche == None:
        return ScheduleResult.NOT_EXISTS

    if sche.owner_id != get_user().id:
        return ScheduleResult.NOT_OWNER

    db.session.delete(sche)
    try:
        db.session.commit()
    except:
        return ScheduleResult.DB_ERROR
    return ScheduleResult.SUCCESS