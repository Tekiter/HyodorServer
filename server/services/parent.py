from sqlalchemy.exc import IntegrityError

from .. import db
from ..model import User, Schedule
from .login import login_required, get_userinfo, get_user, UserPermission


class ParentResult:
    SUCCESS = 0
    INTERNAL_ERROR = 30
    NOT_EXISTS = 11
    DB_ERROR = 5
    NOT_OWNER = 12


    
